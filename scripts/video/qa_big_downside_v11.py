#!/usr/bin/env python3
"""Validate the photographic revision against v9 audio and retained visuals."""
import json
import build_big_downside_v11 as version
import qa_big_downside_v8 as qa

qa.OUT=version.build.OUT
qa.BASE=version.build.BASE
qa.DEST=version.build.DEST

if __name__=='__main__':
    qa.main()
    path=qa.OUT/'qa.json'
    result=json.loads(path.read_text())
    for streams in result['audio'].values():
        streams['base_v9']=streams.pop('v7')
        streams['output_v11']=streams.pop('v8')
    path.write_text(json.dumps(result,indent=2))
