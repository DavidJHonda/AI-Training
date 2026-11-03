#!/usr/bin/env python3
import build_pace_of_change_v12 as build
import qa_pace_of_change_v11 as qa

if __name__=='__main__':
    build.configure()
    qa.main()
