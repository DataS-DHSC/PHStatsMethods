## How to use Git in Spyder

```
# get the repo
!git clone [url]
```

### Push changes to Git
```
# see if there are any changes
!git pull
!git status
!git add --all
!git commit -m "MESSAGE"
!git push

```

### Working with branches 
```
# See branch you are currently working on
!git branch

# View all branches in the GitHub repo
!git pull
!git branch -r

# move to a new branch and pull changes so local branch is up-to-date
!git switch branch_name
!git pull

```

### Keep synced with Dev
```
# Move into Dev and pull most recent changes
!git switch Dev
!git pull

# Move back to your branch and merge in Dev
!git switch [your_branch]
!git merge Dev
```
