# How to build bricks

1. Create a brick named `newbrick` from this template
```
gh repo create -p biobricks-ai/brick-template biobricks-ai/newbrick
gh repo clone biobricks-ai/newbrick
cd newbrick
```

2. replace stages/1-stage.R with your own stages
3. replace stages in dvc.yaml with your new stages
4. Build your brick
```
dvc repro # runs new stages
```
5. Push the data to biobricks.ai
```
dvc push -r s3.biobricks.ai 
```
6. commit the brick
```
git add -A && git commit -m "some message"
git push
```
7. monitor the bricktools github action
```

```

