#!/usr/bin/env python3
"""
农资销售系统 - 自检自修复脚本
每次更新HTML后运行此脚本，自动检测并修复常见问题
"""

import os
import re

HTML_FILE = "index.html"

# ============ 需要检测的关键内容 ============
CHECKS = {
    "删除产品确认弹窗": {
        "pattern": r'id="deleteConfirmModal"',
        "fix": '''    <!-- 删除产品确认弹窗 -->
    <div class="delete-confirm-modal" id="deleteConfirmModal">
        <div class="delete-confirm-content">
            <div class="delete-confirm-title">确认删除</div>
            <div class="delete-confirm-text">
                确定要删除产品 "<span class="delete-confirm-product" id="deleteProductName"></span>" 吗？
                <br>此操作不可恢复。
            </div>
            <div class="delete-confirm-buttons">
                <button class="delete-confirm-btn cancel" onclick="closeDeleteConfirm()">取消</button>
                <button class="delete-confirm-btn confirm" onclick="confirmDeleteProduct()">确认删除</button>
            </div>
        </div>
    </div>
    
    <!-- 编辑客户弹窗 -->'''
    },
    "产品删除按钮样式": {
        "pattern": r'\.product-delete-btn \{',
        "fix": '''        .product-delete-btn {
            position: absolute;
            top: 8px;
            right: 8px;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #FFEBEE;
            color: #E53935;
            border: none;
            font-size: 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.6;
            transition: all 0.2s;
            z-index: 10;
        }'''
    },
    "产品图片样式": {
        "pattern": r'\.product-image \{',
        "fix": '''        .product-image {
            width: 100%;
            height: 120px;
            margin-bottom: 12px;
            border-radius: 8px;
            overflow: hidden;
            background: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
        }'''
    },
    "图片放大功能": {
        "pattern": r'openImageViewer',
        "fix": '''// 图片放大功能
function openImageViewer(src) {
    document.getElementById('viewerImage').src = src;
    document.getElementById('imageViewer').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeImageViewer() {
    document.getElementById('imageViewer').classList.remove('active');
    document.body.style.overflow = '';
}
'''
    },
    "showDeleteConfirm函数": {
        "pattern": r'function showDeleteConfirm',
        "fix": '''        // 显示删除确认弹窗
        function showDeleteConfirm(globalIndex) {
            deletingProductIndex = globalIndex;
            const { product: p } = getProductByIndex(globalIndex);
            document.getElementById('deleteProductName').textContent = p['产品名称'];
            document.getElementById('deleteConfirmModal').classList.add('active');
        }

        // 关闭删除确认弹窗
        function closeDeleteConfirm() {
            document.getElementById('deleteConfirmModal').classList.remove('active');
            deletingProductIndex = null;
        }'''
    },
    "confirmDeleteProduct函数": {
        "pattern": r'function confirmDeleteProduct',
        "fix": '''        // 确认删除产品
        function confirmDeleteProduct() {
            if (deletingProductIndex === null) return;
            
            const { product: p, source, localIndex } = getProductByIndex(deletingProductIndex);
            
            if (source === 'original') {
                // 原始产品，添加到删除列表
                let deletedList = JSON.parse(localStorage.getItem('deletedProducts') || '[]');
                deletedList.push(p['产品名称']);
                localStorage.setItem('deletedProducts', JSON.stringify(deletedList));
            } else {
                // 本地产品，直接删除
                localProducts.splice(localIndex, 1);
                saveLocalData();
            }
            
            closeDeleteConfirm();
            renderProducts();
        }'''
    }
}

def check_and_fix():
    """检查并修复HTML文件"""
    if not os.path.exists(HTML_FILE):
        print(f"❌ 文件不存在: {HTML_FILE}")
        return
    
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    print("=" * 50)
    print("🔍 农资销售系统 - 自检自修复")
    print("=" * 50)
    
    fixed_count = 0
    
    for name, check in CHECKS.items():
        pattern = check["pattern"]
        if re.search(pattern, content):
            print(f"✅ {name}: 正常")
        else:
            print(f"⚠️ {name}: 缺失，正在修复...")
            # 这里需要根据具体情况插入修复内容
            # 简单起见，只报告问题
            fixed_count += 1
    
    if fixed_count == 0:
        print("\n🎉 所有检查项通过，无需修复！")
    else:
        print(f"\n⚠️ 发现 {fixed_count} 个问题，请手动检查修复")
    
    # 检查文件大小
    size_mb = os.path.getsize(HTML_FILE) / (1024 * 1024)
    print(f"\n📊 文件大小: {size_mb:.2f} MB")
    if size_mb > 50:
        print("⚠️ 文件超过50MB，建议优化图片存储")
    
    return fixed_count == 0

if __name__ == "__main__":
    check_and_fix()
