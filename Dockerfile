FROM node:24.22.1-alpine
RUN apk update && apk add bash \
    python3.10 \
    python3-pip \
    gcc 

WORKDIR /tmp/app

COPY . .
RUN npm i

# RUN npm run build

EXPOSE 3000

# CMD ["npm", "run", "debug"]

# docker run -it -v E:/Applications/evaluation-studio-builder:/tmp/app -p 3003:3003 studio-builder bash



# docker build -t gcr.io/viewo-g/piper/agent/runner/apps/studio-builder:0.1.21 -f Dockerfile .
# docker push gcr.io/viewo-g/piper/agent/runner/apps/studio-builder:0.1.21

# docker run -it gcr.io/viewo-g/piper/agent/runner/apps/studio-builder:0.1.21 bash
