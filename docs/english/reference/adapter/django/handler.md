---
sidebar_label: handler
title: slack_bolt.adapter.django.handler
---

## `DjangoListenerCompletionHandler`

Bases: ListenerCompletionHandler

Django sets DB connections as a thread-local variable per thread.

If the thread is not managed on the Django app side, the connections won't be released by Django.
This handler releases the connections every time a ThreadListenerRunner execution completes.

## `DjangoListenerStartHandler`

Bases: ListenerStartHandler

Django sets DB connections as a thread-local variable per thread.

If the thread is not managed on the Django app side, the connections won't be released by Django.
This handler releases the connections every time a ThreadListenerRunner execution completes.
