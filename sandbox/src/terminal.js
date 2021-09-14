class Terminal {
    /***
    Terminal is a simple class for an interactive console definitions,
    it holds basic data about the terminal interface
     * @param name name of terminal
     * @param command start command
     * @param args command arguments
     * @param path initial path
     * @param env env variables
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
const Terminals = {
    python: new Terminal('python', 'python3'),
    javascript: new Terminal('Javascript', 'node', ['-i']),
    bash: new Terminal('Bash', 'bash'),
    shell: new Terminal('Shell', 'sh'),
    cmd: new Terminal('Cmd', 'cmd.exe'),
}

export default Terminals

export {
    Terminal, Terminals
}
