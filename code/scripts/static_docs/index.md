# Final Year Project Documentation

This site contains the documentation for this project, please navigate the reference section in the left panel or use the search tool in the top right.

The project consists of three main sections:

 - [Model](./reference/model/index.md)
     + This package contains the code for the reinforcement learning models such as the agents and dynamics.
 - [View](./reference/view/index.md)
     + This package contains the code for the user interface it displays the state of model and allows the user to interact with it.
 - [Controller](./reference/controller/index.md)
     + This package contains the code that links the Model and View. 

and two entry points:

 - [Main](./reference/main.md)
     - This is the main usual entrypoint of the application
 - [Profile](./reference/profile.md)
     - This is a secondary entrypoint that sets up a profiler before starting the application

This documentation site was generated with [mkdocs](https://www.mkdocs.org).


## Documentation Commands

To start a server that will allow you to see the documentation locally.
```Bash 
poetry run mkdocs serve -a localhost:3000
```

To make a new build of the documentation locally.
```Bash 
poetry run mkdocs build
```


