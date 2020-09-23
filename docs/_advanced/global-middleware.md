---
title: Global middleware
lang: en
slug: global-middleware
order: 6
---

Global middleware is run for all incoming events, before any listener middleware. You can add any number of global middleware to your app by passing a `CustomMiddleware` instance to `app.use()`. The middleware function is called with the same arguments as listeners, with an additional `next()` function.

Global and listener middleware both must call `next()` to pass control of the execution chain to the next middleware. 
