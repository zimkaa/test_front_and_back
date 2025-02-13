FROM node:23-bookworm

WORKDIR /app

RUN npm install react react-dom react-router-dom react-hook-form react-spinners

RUN npm install -D vite @vitejs/plugin-react

COPY . .

RUN npm run build

EXPOSE 3005

CMD ["npm", "run", "serve", "--", "--port", "3005", "--host"]
