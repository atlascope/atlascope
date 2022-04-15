FROM yarnpkg/node-yarn:latest

RUN mkdir /web
WORKDIR /web
COPY ./web /web
RUN npm cache clean -f
RUN npm install n -g -q
RUN n stable -q
RUN npm install -q
