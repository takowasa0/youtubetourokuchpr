# ベースイメージ
FROM node:18-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をインストール
COPY package.json .
COPY package-lock.json .
RUN npm install

# ソースコードをコピー
COPY . .

# ビルドを実行
RUN npm run build

# Nginxでフロントエンドを提供
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# ポートを公開
EXPOSE 80

# Nginxを起動
CMD ["nginx", "-g", "daemon off;"]
