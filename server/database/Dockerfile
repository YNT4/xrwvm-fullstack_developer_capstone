
FROM node:22-bookworm-slim

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY app.js review.js dealership.js inventory.js ./
COPY data/ ./data/

ENV NODE_ENV=production

EXPOSE 3030

CMD ["npm", "start"]
