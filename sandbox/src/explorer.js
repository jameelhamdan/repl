import {FileSystemExplorer} from 'file-system-explorer';
import {readFileSync, writeFileSync} from 'fs';

// All user created files should be here
const explorer = new FileSystemExplorer();

class Explorer {
    static rootDirectory = '/home/runner/';
    static fullPath(path) {
        // TODO: Clean path start from ..~/\
        return this.rootDirectory + path
    }

    static getAll() {
        return explorer.getAllFSElementsDetailsFromFileSystem(this.rootDirectory);
    }

    static getFile(path, encoding = 'utf8') {
        return readFileSync(this.fullPath(path));
    }

    static writeFile(path, content) {
        // TODO: find a better way to update file content than rewriting entire file
        return writeFileSync(this.fullPath(path), content, {flag: 'w+'});
    }

    static createDirectory(path) {
        return explorer.createDirectory(this.fullPath(path), true);
    }

    static delete(path) {
        return explorer.deleteDirectory(this.fullPath(path), true);
    }

    static rename(oldPath, newPath) {
        return explorer.renameFile(this.fullPath(oldPath), this.fullPath(newPath),);
    }
}

export {
    Explorer
}
