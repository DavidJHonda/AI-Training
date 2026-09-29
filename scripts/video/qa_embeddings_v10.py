#!/usr/bin/env python3
import qa_embeddings_v8 as qa
import build_embeddings_v10 as build
qa.DEST=build.DEST
qa.OUT=build.OUT
qa.changed=build.changed
if __name__=='__main__':qa.main()
