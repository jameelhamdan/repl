import {spawn} from "node-pty";


class Repl {
    constructor(_console, output_callback = null) {
        this.console = _console;

        this.proc = spawn(this.console.command, this.console.args, {
            name: "xterm",
            cwd: this.console.path,
            env: this.console.env,
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
