# Shoggoth-c
A Gradescope compatible tool for performing automatic assessment of C homework, using static and dynamic analysis. Focuses on providing generic features for assessing systems-level aspects of code submissions.

## Authors
* Mitchell Buckner
* Ruben Acuña


### Config
The config.json is what you need to configure this.

- package_whitelist should contain a list of packages that are allowed, include the chevrons (<>) around the package name
- required_files are all c files the student must submit
- required_headers are all header files the student must submit<br>
- the suite contains all of the test cases. Each one will have a module (name of the python file the test is in), a method (the name of the method running the test or tests), then the list of tests the method runs.
  - Each test must contain a name and the number of points that the test is worth.