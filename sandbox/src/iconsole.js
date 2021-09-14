class IConsole {
    /*
    IConsole is a simple class for an interactive console,
    it holds basic data about the console interface
    */
    constructor(name, command, args = [], path = '/', env = null) {
        this.name = name;
        this.command = command;
        this.args = args;
        this.path = path;
        this.env = env;
    }
}

// TODO: maybe return this configuration in backend?
const IConsoles = {
    Python: new IConsole('Python', 'python3'),
    Javascript: new IConsole('Javascript', 'node', ['-i']),
    Bash: new IConsole('Bash', 'bash'),
    Shell: new IConsole('Shell', 'sh'),
    Cmd: new IConsole('Cmd', 'cmd.exe'),
}

export default IConsoles
