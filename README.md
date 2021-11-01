# atlascope

This project serves as the front-end to the Girder 4-based [atlascope-api](https://github.com/atlascope/atlascope-api). The following features are included:

* `vuetify` installation and configuration
* `axios` installation and configuration
* `vue-router` installation and skeleton boilerplate
* Girder 4 OAuth client library installation and configuration
* A home page containing a working OAuth login / logout button
* Sentry integration (if no DSN is provided, this will be inactive)
* Vue composition API shims
* TypeScript
* Best-practice eslint configuration
* GitHub Actions CI that runs tests, lint, and build

## Project setup
Install [yarn](https://yarnpkg.com/getting-started/install).

```shell
yarn install
```

### Compiles and hot-reloads for development
```shell
yarn run serve
```

### Compiles and minifies for production
```shell
yarn run build
```

### Run your tests
```shell
yarn run test:unit
```

### Lints and fixes files
```shell
yarn run lint
```
