stocktrade/
├── app.py              # Flask 应用
├── frontend/
│   ├── static/         # 静态资源
│   │   ├── css/
│   │   └── js/
│   └── templates/      # HTML 模板
│       └── index.html
├── backend/
│   ├── __init__.py
│   ├── trade/
│   │   ├── __init__.py
│   │   ├── gateway.py      # 交易网关
│   │   └── position.py     # 持仓管理
│   └── market/
│       ├── __init__.py
│       └── marketdata.py   # 行情服务
├── event.py            # 事件定义
├── eventbus.py         # 事件总线  
├── requirements.txt    # 项目依赖
└── Dockerfile          # Dockerfile