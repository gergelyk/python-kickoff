1. Prepare environment

    ```sh
    ./setup.sh
    source venv/bin/activate
    ```

    Now your application can be called...

    ```sh
    # traditionally, as a local module
    kickoff .:demo hello
    
    # traditionally, as a system-available module
    kickoff :demo hello
    
    # traditionally, as a local script
    kickoff demo/__init__.py hello
    ```

    but also...

    ```sh
    # as a local module
    python demo hello
    
    # as a system-available module
    python -m demo hello
    
    # as a local script
    python demo/__main__.py hello
    
    # as a script available in PATH
    demo hello
    ```

2. Freeze (compile) with *pyinstaller*

    ```sh
    make
    ```

    Now your application can be also called as an executable:

    ```sh
    ./dist/demo hello
    ```
