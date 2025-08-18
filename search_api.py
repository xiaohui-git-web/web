from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据 - 实际应用中可以从数据库或文件系统加载
# 这里我们使用前端页面中定义的导航数据结构
nav_data = [
    {
        "group": "运维工具",
        "items": [
            {"title": "zupu-esxi", "icon": "/static/images/esxi.svg", "link": "https://192.168.29.110", "id": 1},
            {"title": "ESXI-70", "icon": "/static/images/esxi.svg", "link": "https://192.168.31.70", "id": 2},
            {"title": "ESXI-71", "icon": "/static/images/esxi.svg", "link": "https://192.168.31.71", "id": 3},
            {"title": "zupu-neo4j", "icon": "/static/images/neo4j.ico", "link": "http://14.103.92.53:7474", "id": 4},
            {"title": "zupu-kibana", "icon": "/static/images/kibana.png", "link": "http://14.103.92.53:5601", "id": 5},
            {"title": "gitlab", "icon": "/static/images/gitlab.png", "link": "https://gitlab.yofoto.cn", "id": 6}
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

# 搜索API端点
@app.route('/search', methods=['GET'])
def search():
    # 获取搜索关键词
    query = request.args.get('q', '')
    if not query:
        return jsonify({"results": []})

    # 执行搜索
    results = []
    for group in nav_data:
        for item in group['items']:
            # 在标题、链接和组名中搜索
            if (query.lower() in item['title'].lower() or
                query.lower() in item['link'].lower() or
                query.lower() in group['group'].lower()):
                # 添加组信息到结果
                result_item = item.copy()
                result_item['group'] = group['group']
                results.append(result_item)

    # 返回搜索结果
    return jsonify({"results": results})

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