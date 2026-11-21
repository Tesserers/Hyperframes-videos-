// Lee los momentos clave de una jugada (intro, decisión, clave, espejo, cierre) para sincronizar el público.
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage();
  await pg.addInitScript(() => { window.__timelines = {}; });
  await pg.goto("file://" + require("path").resolve(process.argv[2]));
  await pg.waitForFunction(() => window.__marks, null, { timeout: 15000 });
  console.log(JSON.stringify(await pg.evaluate(() => window.__marks)));
  await b.close();
})();
