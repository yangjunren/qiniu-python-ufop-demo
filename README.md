# ufop demo

# 构建镜像
进入该目录，然后运行以下命令，获得名为 ufopdemo:v1 的 docker 镜像

```
docker build -t "yjr-ufoptest:v1" .
```

# 验证镜像功能

## 运行镜像

```
docker run -p 9100:9100 yjr-ufoptest:v1
```

## 测试数据处理接口

### 测试处理资源通过url参数来指定：
运行命令

```
curl -X POST "http://127.0.0.1:9100/handler?cmd=yjr-ufoptest&url=http://qiniu.com/4/a1.jpg"

```

来自 http://qiniu.com/4/a1.jpg 的网页内容会被打印

### 健康检查
运行命令

```
curl -v "http://127.0.0.1:9100/health"
```

返回status code为200，响应内容是 health is OK

