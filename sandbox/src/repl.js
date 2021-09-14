import {spawn} from "node-pty";


class Repl {
    constructor(terminal, output_callback = null) {
        this.terminal = terminal;

        this.proc = spawn(this.terminal.command, this.terminal.args, {
            name: "xterm",
            cwd: this.terminal.path,
            env: this.terminal.env,
        });
        this.messages = [];

        this.proc.on('data', data => {
            this.messages.push(data);
            if (typeof output_callback === "function") output_callback(data);
        });
    }

    write(data) {
        this.proc.write(data);
    }

    execute(data) {
        this.proc.write(data);
    }

    kill() {
        this.proc.removeAllListeners('data');
        this.proc.kill()
    }
}

export default Repl;
