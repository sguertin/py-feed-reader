# py-feed-reader

A personal project to build my own rss reader using feedparser and other python libraries

## Dependencies

```txt
    feedparser==6.0.12
```

## Major Features

1. Interactive Reader   - IN PROGRESS
1. Web App              - IN DESIGN
1. TUI Reader           - UNCOMMITTED
1. GUI App              - UNCOMMITTED

### 1. Interactive Reader

The goal of this implementation is to build a python object, or objects, that can serve as an interface for an RSS Reader.

#### Core Functions

- Maintain a list of xml feeds and read items for each
  - Be able to alias those feeds to any name if desired
  - Be able to browse, filter, and sort the list
  - Store a local copy of feed item information

### 2. Web App

A basic web application that will serve as a front end over the reader, potentially using flask, FastAPI, or even microdot

### 3. TUI Reader

A CLI-based reader, perhaps using a library like Textual

### 4. GUI App

A GUI application that will serve as a front end over the reader, possibly using FreeSimpleGUI.
