FROM node:16

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --yes \
 git

RUN git clone https://github.com/Kitware/glance.git
WORKDIR /glance
RUN npm install
RUN npm run build

EXPOSE 9999
ENTRYPOINT [ "/usr/local/bin/npm", "run", "dev" ]
