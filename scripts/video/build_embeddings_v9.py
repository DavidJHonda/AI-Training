#!/usr/bin/env python3
"""Final visual repair; v8's cleanup refined to remove both parentheses."""
import build_embeddings_v8 as base

base.DEST=base.ROOT/'Prompts/embeddings-v9.mp4'
base.OUT=base.ROOT/'video-audit/embeddings-repair-2026-09-29-v9'

def taste(im):
    ans=im.copy()
    ans[660:720,1170:1280]=im[590:650,1170:1280]
    return ans

base.taste=taste

if __name__=='__main__':base.main()
