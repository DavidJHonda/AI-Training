#!/usr/bin/env python3
import build_embeddings_v14 as build
import qa_embeddings_v13 as qa
qa.DEST=build.base.DEST
qa.STATES=build.base.STATES
if __name__=='__main__':qa.main()
