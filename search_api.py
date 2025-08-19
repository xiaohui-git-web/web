from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据 - 实际应用中可以从数据库或文件系统加载
# 这里我们使用前端页面中定义的导航数据结构
nav_data = [
    {
        "group": "运维工具",
        "items": [
            {"title": "堡垒机", "icon": "/static/images/堡垒机.png", "link": "https://192.168.0.98", "id": 0},
            {"title": "zupu-esxi", "icon": "/static/images/esxi.svg", "link": "https://192.168.29.110", "id": 1},
            {"title": "ESXI-70", "icon": "/static/images/esxi.svg", "link": "https://192.168.31.70", "id": 2},
            {"title": "ESXI-71", "icon": "/static/images/esxi.svg", "link": "https://192.168.31.71", "id": 3},
            {"title": "zupu-neo4j", "icon": "/static/images/neo4j.ico", "link": "http://14.103.92.53:7474", "id": 4},
            {"title": "zupu-kibana", "icon": "/static/images/kibana.png", "link": "http://14.103.92.53:5601", "id": 5},
            {"title": "gitlab", "icon": "/static/images/gitlab.png", "link": "https://gitlab.yofoto.cn", "id": 6},
            {"title": "火山云", "icon": "/static/images/火山引擎.png", "link": "https://www.volcengine.com/", "id": 25},
            {"title": "超融合", "icon": "/static/images/超融合.png", "link": "http://192.168.5.10:5000", "id": 26}
        ]
    },
    {
        "group": "监控",
        "items": [
            {"title": "夜莺", "icon": "/static/images/夜莺.png", "link": "http://192.168.0.63:17000", "id": 7},
            {"title": "内网-Prom", "icon": "/static/images/prometheus.png", "link": "http://192.168.7.76:9090", "id": 8},
            {"title": "zupu-Prom", "icon": "/static/images/prometheus.png", "link": "http://14.103.92.53:9090", "id": 9},
            {"title": "夜莺-Prom", "icon": "/static/images/prometheus.png", "link": "http://192.168.0.63:9090", "id": 10},
            {"title": "yihai-Prom", "icon": "/static/images/prometheus.png", "link": "http://14.103.162.150:9090", "id": 11},
            {"title": "派享云-Prom", "icon": "/static/images/prometheus.png", "link": "http://14.103.162.150:9090", "id": 12},
            {"title": "蜂鸟部落-Prom", "icon": "/static/images/prometheus.png", "link": "http://14.103.92.163:9090", "id": 13},
            {"title": "网络-Prom", "icon": "/static/images/prometheus.png", "link": "http://192.168.7.187:9090", "id": 14},
            {"title": "内网-grafana", "icon": "/static/images/grafana.png", "link": "http://192.168.7.76:3000", "id": 15},
            {"title": "zupu-grafana", "icon": "/static/images/grafana.png", "link": "http://14.103.92.53:3000", "id": 16},
            {"title": "夜莺-grafana", "icon": "/static/images/grafana.png", "link": "http://192.168.0.63:3000", "id": 17},
            {"title": "网络-grafana", "icon": "/static/images/grafana.png", "link": "http://192.168.7.187:3000", "id": 18}
        ]
    },
    {
        "group": "工具",
        "items": [
            {"title": "密码工具", "icon": "/static/images/密码.png", "link": "https://mima.yofoto.com", "id": 19},
            {"title": "closeai", "icon": "/static/images/closeai.png", "link": "https://www.closeai-asia.com", "id": 20},
            {"title": "dootask", "icon": "/static/images/dootask.png", "link": "http://dootask.yofoto.cn/", "id": 21},
            {"title": "oa", "icon": "/static/images/oa.png", "link": "https://oa.yofoto.cn/", "id": 22},
            {"title": "邮箱", "icon": "/static/images/邮箱.png", "link": "https://mail.yofoto.cn/", "id": 23},
            {"title": "nginx-web", "icon": "/static/images/nginx-web.ico", "link": "http://192.168.4.50:8000", "id": 24}
        ]
    }
]

# 搜索API端点 - 支持中文搜索
@app.route('/search', methods=['GET'])
def search():
    # 获取搜索关键词并确保UTF-8编码
    query = request.args.get('q', '', type=str)
    if not query:
        return jsonify({"results": []})

    # 执行搜索
    results = []
    # 转换为小写以实现大小写不敏感搜索
    query_lower = query.lower()
    for group in nav_data:
        group_name_lower = group['group'].lower()
        if query_lower in group_name_lower:
            # 如果组名匹配，添加组内所有项目
            for item in group['items']:
                result_item = item.copy()
                result_item['group'] = group['group']
                results.append(result_item)
        else:
            # 否则搜索组内项目
            for item in group['items']:
                title_lower = item['title'].lower()
                link_lower = item['link'].lower()
                if (query_lower in title_lower or
                    query_lower in link_lower):
                    result_item = item.copy()
                    result_item['group'] = group['group']
                    results.append(result_item)

    # 移除了模糊匹配逻辑，避免不相关结果
    # 如果没有精确匹配，返回空结果
    

    # 返回搜索结果
    return jsonify({"results": results})

# 添加新数据条目的API端点
@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'error': '没有提供数据'}), 400

        # 验证必要字段
        required_fields = ['group', 'title', 'icon', 'link']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必要字段: {field}'}), 400

        # 查找组
        group_name = data['group']
        group_found = False
        for group in nav_data:
            if group['group'] == group_name:
                # 生成新ID (当前最大ID + 1)
                max_id = max(item['id'] for item in group['items']) if group['items'] else 0
                new_id = max_id + 1

                # 创建新条目
                new_item = {
                    'title': data['title'],
                    'icon': data['icon'],
                    'link': data['link'],
                    'id': new_id
                }

                # 添加到组
                group['items'].append(new_item)
                group_found = True
                break

        # 如果组不存在，创建新组
        if not group_found:
            # 生成新ID
            new_id = 0
            for group in nav_data:
                if group['items']:
                    group_max_id = max(item['id'] for item in group['items'])
                    new_id = max(new_id, group_max_id)
            new_id += 1

            # 创建新组和条目
            new_group = {
                'group': group_name,
                'items': [{
                    'title': data['title'],
                    'icon': data['icon'],
                    'link': data['link'],
                    'id': new_id
                }]
            }
            nav_data.append(new_group)

        # 返回成功响应
        return jsonify({'success': True, 'message': '数据条目添加成功'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 允许跨域请求的中间件
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    # 启动Flask服务器
    app.run(host='0.0.0.0', port=5000, debug=True)