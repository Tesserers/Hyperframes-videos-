import fs from 'node:fs';
import { Config } from '@remotion/cli/config';

// En el contenedor de Claude hay un Chromium preinstalado; en tu máquina
// Remotion descarga el suyo y esta línea no hace nada.
const preinstalled = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
if (fs.existsSync(preinstalled)) Config.setBrowserExecutable(preinstalled);

Config.setVideoImageFormat('png');
Config.setOverwriteOutput(true);
