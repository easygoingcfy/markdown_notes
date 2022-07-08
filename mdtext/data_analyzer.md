使用vis_db

```
python3 modules/tools/data_analyzer/vis_db.py list_records /fabupilot/data/log/2022-06-08/db/2022-06-08.db --tables event
```

基于公司rc-x.x生成版本：

```
git checkout master
git reset --hard f9ba186b2700648c97d1a80878ea0bc5b12dcc44
git merge --squash dc_test
git cmm "add new module data collect"
git checkout data_analyzer_v2.6
git reset --hard d23ddef3951861af84c9406e4bbf24dbd2b8af1c
git cherrypick 


```

目前子模块版本号

```
deploy：
ce69ec649a089e56b63efe3a7cf37989ac6d3141
fabupilot_config:
11a5fe9b9670826041b728ccc2568bec3ddb6502
planning_v3：
4e37907d3b51cf42f00e33bc9bb68a19d1475515
data_analyzer 
d1a620015ba060a2733f85c1e6304cc6caaace91
```

```
基于v2.6 直接在v2.6merge 5g_delay  11:34
custom_builds/02c1cc35
x86:3931
arm:3931
```

