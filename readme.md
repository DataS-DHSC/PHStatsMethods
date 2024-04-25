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

### Running tests
(may need to install pytest first - !pip install pytest)
```
# run all tests
!pytest

# run all tests in file
!pytest tests/file.py

# run test function (outside of class)
!pytest tests/file.py::TestFunction

# run test class
!pytest tests/file.py::TestClass

# run test method (a method is a function in a class)
!pytest tests/file.py::TestClass::TestMethod
```

### Running a module (with relative paths)
```
# in terminal - class notation NOT file (.py)
python -m ph_statistical_methods.rates
