from flask import Flask, request, jsonify
from knowlegebase.DifyIntegration import DifyIntegration  # 导入你的类
import os

app = Flask(__name__)
dify_client = DifyIntegration(dataset_id="your_dataset_id")  # 初始化客户端

@app.route('/upload', methods=['POST'])
def upload_api():
    """
    处理文件上传API请求，将文档上传到指定数据集

    Args:
        无显式参数，通过Flask request对象获取以下内容:
        - file: 上传的文件对象 (multipart/form-data)
        - dataset_id: 查询参数，目标数据集的唯一标识符
        - file_type: 表单参数，文件类型(可选，默认'auto')

    Returns:
        JSON响应:
        - 成功: 200状态码，包含操作结果
        - 参数错误: 400状态码，错误信息
        - 异常错误: 500状态码，异常信息
    """
    try:
        # 处理文件上传核心逻辑
        # 从请求中提取二进制文件对象，必须包含file字段
        uploaded_file = request.files['file']

        # 关键参数校验逻辑
        # 从URL参数获取数据集ID，必须参数缺失时返回错误
        dataset_id = request.args.get('dataset_id', default='')
        if dataset_id == '':
            return jsonify({
                "status": "error",
                "message": "dataset_id is required"
            }), 400

        # 获取可选文件类型参数，默认自动检测
        file_type = request.form.get('file_type', 'auto')

        # 临时文件处理逻辑
        # 在系统临时目录创建同名文件保存上传内容
        temp_path = f"/tmp/{uploaded_file.filename}"
        uploaded_file.save(temp_path)

        # 业务逻辑处理
        # 调用数据平台接口上传文档到指定数据集
        result = dify_client.upload_document(dataset_id, temp_path, file_type)

        # 资源清理
        # 确保操作完成后删除临时文件
        os.remove(temp_path)

        # 成功响应处理
        # 包装平台接口返回的原始结果
        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        # 全局异常处理
        # 捕获所有未处理异常并返回标准化错误格式
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
