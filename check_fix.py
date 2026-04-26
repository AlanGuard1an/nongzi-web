#!/usr/bin/env python3
"""
农资销售系统 - 自检自修复脚本
自动检测并修复HTML文件中的常见问题
"""

import os
import re
from datetime import datetime

HTML_FILE = "index.html"
REPORT_FILE = "检测报告.txt"

# ============ 检测项配置 ============
CHECKS = [
    {
        "name": "删除产品确认弹窗",
        "pattern": r'id="deleteConfirmModal"',
        "type": "html",
        "insert_before": r'    <!-- 编辑客户弹窗 -->',
        "content": '''    <!-- 删除产品确认弹窗 -->
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
    
    '''
    },
    {
        "name": "图片放大遮罩",
        "pattern": r'id="imageViewer"',
        "type": "html",
        "insert_before": r'</body>',
        "content": '''<!-- 图片放大遮罩 -->
<div class="image-viewer" id="imageViewer" onclick="closeImageViewer()">
    <span class="image-viewer-close">&times;</span>
    <img id="viewerImage" src="" alt="放大图片">
</div>

'''
    },
    {
        "name": "产品删除按钮",
        "pattern": r'showDeleteConfirm\(\$\{globalIndex\}\)',
        "type": "code",
        "fallback": "需检查产品列表渲染函数"
    },
    {
        "name": "删除确认函数",
        "pattern": r'function confirmDeleteProduct',
        "type": "code",
        "fallback": "需添加删除确认函数"
    },
    {
        "name": "图片放大函数",
        "pattern": r'function openImageViewer',
        "type": "code",
        "fallback": "需添加图片放大函数"
    },
    {
        "name": "产品列表渲染",
        "pattern": r'function renderProducts',
        "type": "code",
        "fallback": "产品列表渲染函数缺失"
    },
    {
        "name": "客户编辑功能",
        "pattern": r'function openEditCustomer',
        "type": "code",
        "fallback": "客户编辑功能缺失"
    },
    {
        "name": "铺货记录功能",
        "pattern": r'function openAddCustomerProduct',
        "type": "code",
        "fallback": "铺货记录功能缺失"
    }
]

def run_check():
    """运行检测并生成报告"""
    if not os.path.exists(HTML_FILE):
        return "❌ 文件不存在: index.html"
    
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 生成报告
    report = []
    report.append("=" * 50)
    report.append(f"📋 农资销售系统 - 检测报告")
    report.append(f"⏰ 检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 50)
    report.append("")
    
    issues = []
    fixed = []
    
    for check in CHECKS:
        name = check["name"]
        pattern = check["pattern"]
        
        if re.search(pattern, content):
            report.append(f"✅ {name}")
        else:
            report.append(f"❌ {name} - 缺失")
            issues.append(check)
    
    # 文件信息
    size_mb = len(content) / (1024 * 1024)
    report.append("")
    report.append("-" * 50)
    report.append(f"📊 文件大小: {size_mb:.2f} MB")
    
    if size_mb > 50:
        report.append("⚠️  警告: 文件超过50MB")
    
    # 尝试自动修复
    if issues:
        report.append("")
        report.append("-" * 50)
        report.append("🔧 尝试自动修复...")
        
        for issue in issues:
            if "insert_before" in issue and "content" in issue:
                insert_pattern = issue["insert_before"]
                if re.search(insert_pattern, content):
                    content = re.sub(insert_pattern, issue["content"] + re.search(insert_pattern, content).group(), content, count=1)
                    report.append(f"   ✅ 已修复: {issue['name']}")
                    fixed.append(issue["name"])
        
        # 保存修复后的文件
        if fixed:
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(content)
    
    # 总结
    report.append("")
    report.append("=" * 50)
    total = len(CHECKS)
    passed = total - len(issues) + len(fixed)
    report.append(f"📈 检测结果: {passed}/{total} 项通过")
    
    if len(issues) == 0:
        report.append("🎉 所有检测项通过！")
    elif len(fixed) == len(issues):
        report.append("✅ 所有问题已自动修复！")
    else:
        remaining = len(issues) - len(fixed)
        report.append(f"⚠️  还有 {remaining} 项需要手动检查")
    
    report.append("=" * 50)
    
    # 保存报告
    report_text = "\n".join(report)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    return report_text

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(run_check())
