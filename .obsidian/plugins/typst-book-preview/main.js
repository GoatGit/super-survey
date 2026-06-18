/* THIS FILE IS GENERATED FROM main.ts. */
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// main.ts
var main_exports = {};
__export(main_exports, {
  default: () => TypstBookPreviewPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian = require("obsidian");
var import_child_process = require("child_process");
var import_fs = require("fs");
var path = __toESM(require("path"));
var VIEW_TYPE_TYPST_BOOK_PREVIEW = "typst-book-preview";
var DEFAULT_TOOLBAR_GROUPS = {
  basic: true,
  text: true,
  notes: true,
  headings: true,
  lists: true,
  layout: true,
  objects: true,
  templates: true
};
var DEFAULT_SETTINGS = {
  typstCommand: "typst",
  mainTypstPath: "book.typ",
  showTypstToolbar: true,
  toolbarGroups: { ...DEFAULT_TOOLBAR_GROUPS }
};
var TYPST_TOOLBAR_GROUP_OPTIONS = [
  { id: "basic", name: "Basic text", description: "Emphasis, strong, raw text, math, highlight, underline, strike, subscript, superscript, and links." },
  { id: "text", name: "Text refinements", description: "Small capitals, overline, uppercase, and lowercase." },
  { id: "notes", name: "Notes and references", description: "Footnotes, quotes, labels, references, and citations." },
  { id: "headings", name: "Headings", description: "Heading levels H1 through H6." },
  { id: "lists", name: "Lists and comments", description: "Bullet, numbered, term-list, and line-comment prefixes." },
  { id: "layout", name: "Layout", description: "Outline, page break, and columns." },
  { id: "objects", name: "Objects", description: "Figure, table, and bibliography snippets." },
  { id: "templates", name: "Templates", description: "Paperback book and article/report starters." }
];
var DEFAULT_STATE = {
  status: "idle",
  message: "Ready",
  errorText: "",
  pdfPath: null,
  updatedAt: null
};
var IMAGE_EXTENSIONS = /* @__PURE__ */ new Set(["png", "jpg", "jpeg", "webp", "svg", "gif"]);
var PAPERBACK_TEMPLATE = `#set page(
  width: 5.5in,
  height: 8.5in,
  margin: (
    inside: 0.8in,
    outside: 0.55in,
    top: 0.65in,
    bottom: 0.75in,
  ),
  binding: left,
  numbering: "1",
)
#set text(size: 10.5pt)
#set par(justify: true, first-line-indent: 1.2em)
#set heading(numbering: "1.")

#align(center)[
  #text(18pt)[Title]
  #v(0.5em)
  Author
]

#pagebreak()
#outline(title: [Contents])
#pagebreak()

= Chapter One

First paragraph.
`;
var ARTICLE_TEMPLATE = `#set page("us-letter", margin: 1in, numbering: "1")
#set text(size: 11pt)
#set par(justify: true)

#align(center)[
  #text(16pt, weight: "bold")[Title] \\
  Author
]

#v(1em)

= Introduction

First paragraph.

// #bibliography("works.bib")
`;
var TYPST_TOOLBAR_TOOLS = [
  { label: "_", title: "Emphasis", group: "basic", prefix: "_", suffix: "_" },
  { label: "*", title: "Strong", group: "basic", prefix: "*", suffix: "*" },
  { label: "`", title: "Raw text", group: "basic", prefix: "`", suffix: "`" },
  { label: "$", title: "Math", group: "basic", prefix: "$", suffix: "$" },
  { label: "H", title: "Highlight", group: "basic", prefix: "#highlight[", suffix: "]" },
  { label: "U", title: "Underline", group: "basic", prefix: "#underline[", suffix: "]" },
  { label: "S", title: "Strike", group: "basic", prefix: "#strike[", suffix: "]" },
  { label: "sub", title: "Subscript", group: "basic", prefix: "#sub[", suffix: "]" },
  { label: "sup", title: "Superscript", group: "basic", prefix: "#super[", suffix: "]" },
  { label: "link", title: "Link", group: "basic", prefix: '#link("")[', suffix: "]", cursorOffset: 7 },
  { label: "sc", title: "Small capitals", group: "text", prefix: "#smallcaps[", suffix: "]", separatorBefore: true },
  { label: "ovr", title: "Overline", group: "text", prefix: "#overline[", suffix: "]" },
  { label: "up", title: "Uppercase", group: "text", prefix: "#upper[", suffix: "]" },
  { label: "lo", title: "Lowercase", group: "text", prefix: "#lower[", suffix: "]" },
  { label: "Fn", title: "Footnote", group: "notes", prefix: "#footnote[", suffix: "]", separatorBefore: true },
  { label: "Q", title: "Block quote", group: "notes", prefix: "#quote(block: true)[\n", suffix: "\n]" },
  { label: "<>", title: "Label", group: "notes", prefix: "<", suffix: ">" },
  { label: "@", title: "Reference", group: "notes", prefix: "@", suffix: "" },
  { label: "cite", title: "Citation", group: "notes", prefix: "#cite(<", suffix: ">)" },
  { label: "H1", title: "Heading 1", group: "headings", kind: "line-prefix", linePrefix: "= ", separatorBefore: true },
  { label: "H2", title: "Heading 2", group: "headings", kind: "line-prefix", linePrefix: "== " },
  { label: "H3", title: "Heading 3", group: "headings", kind: "line-prefix", linePrefix: "=== " },
  { label: "H4", title: "Heading 4", group: "headings", kind: "line-prefix", linePrefix: "==== " },
  { label: "H5", title: "Heading 5", group: "headings", kind: "line-prefix", linePrefix: "===== " },
  { label: "H6", title: "Heading 6", group: "headings", kind: "line-prefix", linePrefix: "====== " },
  { label: "-", title: "Bullet list item", group: "lists", kind: "line-prefix", linePrefix: "- " },
  { label: "+", title: "Numbered list item", group: "lists", kind: "line-prefix", linePrefix: "+ " },
  { label: "/", title: "Term list item", group: "lists", kind: "line-prefix", linePrefix: "/ " },
  { label: "//", title: "Line comment", group: "lists", kind: "line-prefix", linePrefix: "// " },
  { label: "TOC", title: "Outline", group: "layout", kind: "insert", text: "#outline()\n", separatorBefore: true },
  { label: "Pg", title: "Page break", group: "layout", kind: "insert", text: "#pagebreak()\n" },
  { label: "Col", title: "Columns", group: "layout", prefix: "#columns(2, gutter: 1em)[\n", suffix: "\n]" },
  { label: "Fig", title: "Figure", group: "objects", prefix: "#figure(\n  [", suffix: "],\n  caption: [Caption],\n) <fig:label>" },
  {
    label: "Tbl",
    title: "Table",
    group: "objects",
    kind: "insert",
    text: "#table(\n  columns: 2,\n  table.header([Header 1], [Header 2]),\n  [Cell 1], [Cell 2],\n)\n",
    cursorOffset: "#table(\n  columns: ".length
  },
  {
    label: "Bib",
    title: "Bibliography",
    group: "objects",
    kind: "insert",
    text: '#bibliography("works.bib")\n',
    cursorOffset: '#bibliography("'.length
  },
  {
    label: "Book",
    title: "Paperback book template",
    group: "templates",
    kind: "insert",
    text: PAPERBACK_TEMPLATE,
    cursorOffset: PAPERBACK_TEMPLATE.indexOf("Title")
  },
  {
    label: "Art",
    title: "Article/report template",
    group: "templates",
    kind: "insert",
    text: ARTICLE_TEMPLATE,
    cursorOffset: ARTICLE_TEMPLATE.indexOf("Title")
  }
];
var TypstBookPreviewPlugin = class extends import_obsidian.Plugin {
  settings = {
    ...DEFAULT_SETTINGS,
    toolbarGroups: { ...DEFAULT_TOOLBAR_GROUPS }
  };
  state = { ...DEFAULT_STATE };
  compileTimer = null;
  compileRunning = false;
  compileQueued = false;
  toolbarManager = null;
  async onload() {
    await this.loadSettings();
    this.toolbarManager = new TypstToolbarManager(this);
    this.toolbarManager.start();
    this.registerView(
      VIEW_TYPE_TYPST_BOOK_PREVIEW,
      (leaf) => new TypstBookPreviewView(leaf, this)
    );
    this.addRibbonIcon("book-open", "Open Typst Book Preview", () => {
      void this.activateView();
    });
    this.addCommand({
      id: "open-typst-book-preview",
      name: "Open preview",
      callback: () => {
        void this.activateView();
      }
    });
    this.addCommand({
      id: "compile-typst-book",
      name: "Compile",
      callback: () => {
        void this.compile("manual");
      }
    });
    this.addCommand({
      id: "use-active-file-as-main-typst-book",
      name: "Use active file as main file",
      checkCallback: (checking) => {
        const activeFile = this.app.workspace.getActiveFile();
        if (!activeFile || !isTypstSourcePath(activeFile.path)) {
          return false;
        }
        if (!checking) {
          void this.setMainTypstPath(activeFile.path);
          new import_obsidian.Notice(`Typst Book Preview: main file set to ${activeFile.path}`);
        }
        return true;
      }
    });
    this.registerEvent(
      this.app.vault.on("modify", (file) => {
        if (this.shouldCompileOnModify(file)) {
          this.scheduleCompile("save");
        }
      })
    );
    this.registerEvent(
      this.app.vault.on("rename", (file, oldPath) => {
        if (!(file instanceof import_obsidian.TFile) || !this.getMainInputCandidates().includes(oldPath)) {
          return;
        }
        void this.setMainTypstPath(file.path);
        new import_obsidian.Notice(`Typst Book Preview: main file moved to ${file.path}`);
      })
    );
    this.addSettingTab(new TypstBookPreviewSettingTab(this.app, this));
  }
  onunload() {
    if (this.compileTimer !== null) {
      window.clearTimeout(this.compileTimer);
      this.compileTimer = null;
    }
    this.toolbarManager?.removeToolbar();
  }
  async activateView() {
    const existingLeaf = this.app.workspace.getLeavesOfType(VIEW_TYPE_TYPST_BOOK_PREVIEW)[0];
    if (existingLeaf) {
      this.app.workspace.revealLeaf(existingLeaf);
      return;
    }
    const leaf = this.app.workspace.getRightLeaf(false) ?? this.app.workspace.getLeaf(true);
    await leaf.setViewState({
      type: VIEW_TYPE_TYPST_BOOK_PREVIEW,
      active: true
    });
    this.app.workspace.revealLeaf(leaf);
  }
  scheduleCompile(reason, delayMs = 250) {
    if (this.compileTimer !== null) {
      window.clearTimeout(this.compileTimer);
    }
    this.compileTimer = window.setTimeout(() => {
      this.compileTimer = null;
      void this.compile(reason);
    }, delayMs);
  }
  async compile(reason) {
    if (this.compileRunning) {
      this.compileQueued = true;
      return;
    }
    this.compileRunning = true;
    this.compileQueued = false;
    let compilePaths;
    try {
      compilePaths = this.resolveCompilePaths();
    } catch (error) {
      const errorText = errorToString(error);
      this.setState({
        status: "error",
        message: "Typst compile could not start.",
        errorText,
        updatedAt: Date.now()
      });
      if (reason === "manual") {
        await this.activateView();
      }
      new import_obsidian.Notice("Typst Book Preview: compile could not start.");
      this.finishCompile();
      return;
    }
    this.setState({
      status: "compiling",
      message: `Compiling ${compilePaths.inputVaultPath}...`,
      errorText: "",
      updatedAt: Date.now()
    });
    try {
      const command = this.getTypstCommand();
      const result = await execFilePromise(
        command,
        [
          "compile",
          "--root",
          compilePaths.vaultBasePath,
          compilePaths.inputAbsolutePath,
          compilePaths.outputAbsolutePath
        ],
        {
          cwd: compilePaths.workingDirectory,
          encoding: "utf8",
          env: { ...process.env, NO_COLOR: "1" },
          maxBuffer: 10 * 1024 * 1024,
          timeout: 6e4
        }
      );
      const compilerOutput = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
      this.setState({
        status: "success",
        message: this.successMessage(reason, compilePaths.outputVaultPath),
        errorText: compilerOutput,
        pdfPath: compilePaths.outputVaultPath,
        updatedAt: Date.now()
      });
    } catch (error) {
      this.setState({
        status: "error",
        message: "Typst compile failed.",
        errorText: compilerErrorToString(error),
        updatedAt: Date.now()
      });
      if (reason === "manual") {
        await this.activateView();
      }
      new import_obsidian.Notice("Typst Book Preview: Typst compile failed.");
    } finally {
      this.finishCompile();
    }
  }
  shouldCompileOnModify(file) {
    if (!(file instanceof import_obsidian.TFile)) {
      return false;
    }
    if (isTypstSourcePath(file.path)) {
      if (this.getMainInputCandidates().includes(file.path)) {
        return true;
      }
      return this.isInBookRoot(file.path);
    }
    if (isImageAssetPath(file.path)) {
      return this.isInBookRoot(file.path);
    }
    return false;
  }
  getMainTypstPath() {
    return (0, import_obsidian.normalizePath)(this.settings.mainTypstPath.trim() || DEFAULT_SETTINGS.mainTypstPath);
  }
  getOutputPdfPath() {
    return getOutputPdfPath(this.getMainTypstPath());
  }
  getDisplayTypstCommand() {
    return this.settings.typstCommand.trim() || DEFAULT_SETTINGS.typstCommand;
  }
  diagnosticText() {
    const lines = [
      this.state.message,
      `Main file: ${this.getMainTypstPath()}`,
      `Output PDF: ${this.getOutputPdfPath()}`,
      `Typst command: ${this.getDisplayTypstCommand()}`
    ];
    if (this.state.updatedAt) {
      lines.push(`Updated: ${new Date(this.state.updatedAt).toLocaleString()}`);
    }
    if (this.state.errorText) {
      lines.push("", this.state.errorText);
    }
    return lines.join("\n");
  }
  async loadSettings() {
    const loaded = await this.loadData();
    this.settings = {
      ...DEFAULT_SETTINGS,
      ...loaded ?? {},
      toolbarGroups: {
        ...DEFAULT_TOOLBAR_GROUPS,
        ...loaded?.toolbarGroups ?? {}
      }
    };
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  async setMainTypstPath(vaultPath) {
    this.settings.mainTypstPath = (0, import_obsidian.normalizePath)(vaultPath);
    await this.saveSettings();
    await this.refreshViews();
  }
  async refreshViews() {
    for (const leaf of this.app.workspace.getLeavesOfType(VIEW_TYPE_TYPST_BOOK_PREVIEW)) {
      if (leaf.view instanceof TypstBookPreviewView) {
        leaf.view.render();
      }
    }
  }
  refreshTypstToolbar() {
    this.toolbarManager?.refresh();
  }
  isTypstToolbarGroupEnabled(group) {
    return this.settings.toolbarGroups[group] ?? DEFAULT_TOOLBAR_GROUPS[group];
  }
  finishCompile() {
    this.compileRunning = false;
    if (this.compileQueued) {
      this.scheduleCompile("queued", 100);
    }
  }
  setState(nextState) {
    this.state = {
      ...this.state,
      ...nextState
    };
    void this.refreshViews();
  }
  successMessage(reason, outputPath) {
    if (reason === "save" || reason === "queued") {
      return `Compiled on save: ${outputPath}`;
    }
    return `Compiled: ${outputPath}`;
  }
  resolveCompilePaths() {
    const inputVaultPath = this.getMainTypstPath();
    validateVaultPath(inputVaultPath, "Main Typst file");
    if (!isTypstSourcePath(inputVaultPath)) {
      throw new Error("Main Typst file must end with .typ or .typ.md.");
    }
    const inputFile = this.getMainInputCandidates().map((candidatePath) => this.app.vault.getAbstractFileByPath(candidatePath)).find((file) => file instanceof import_obsidian.TFile);
    if (!(inputFile instanceof import_obsidian.TFile)) {
      throw new Error(this.notFoundMessage(inputVaultPath));
    }
    const outputVaultPath = getOutputPdfPath(inputVaultPath);
    validateVaultPath(outputVaultPath, "Output PDF");
    const vaultBasePath = getVaultBasePath(this.app);
    const inputAbsolutePath = resolveInsideVault(vaultBasePath, inputFile.path);
    const outputAbsolutePath = resolveInsideVault(vaultBasePath, outputVaultPath);
    return {
      vaultBasePath,
      inputVaultPath: inputFile.path,
      outputVaultPath,
      inputAbsolutePath,
      outputAbsolutePath,
      workingDirectory: path.dirname(inputAbsolutePath)
    };
  }
  getTypstCommand() {
    const configuredCommand = this.settings.typstCommand.trim() || DEFAULT_SETTINGS.typstCommand;
    if (configuredCommand !== DEFAULT_SETTINGS.typstCommand) {
      return configuredCommand;
    }
    for (const candidate of ["/opt/homebrew/bin/typst", "/usr/local/bin/typst"]) {
      if ((0, import_fs.existsSync)(candidate)) {
        return candidate;
      }
    }
    return configuredCommand;
  }
  getBookRootPath() {
    const inputPath = this.getMainTypstPath();
    const lastSlash = inputPath.lastIndexOf("/");
    return lastSlash === -1 ? "" : inputPath.slice(0, lastSlash);
  }
  getMainInputCandidates() {
    const mainPath = this.getMainTypstPath();
    if (mainPath.toLowerCase().endsWith(".typ")) {
      return [mainPath, `${mainPath}.md`];
    }
    return [mainPath];
  }
  isInBookRoot(vaultPath) {
    const bookRoot = this.getBookRootPath();
    return bookRoot === "" || vaultPath.startsWith(`${bookRoot}/`);
  }
  notFoundMessage(inputVaultPath) {
    const checkedPaths = this.getMainInputCandidates().join(", ");
    if (inputVaultPath.toLowerCase().endsWith(".typ")) {
      return `Main Typst file was not found in the vault. Checked: ${checkedPaths}. If you created it with Obsidian's New note command, it may exist on disk as ${inputVaultPath}.md.`;
    }
    return `Main Typst file was not found in the vault: ${inputVaultPath}`;
  }
};
var TypstToolbarManager = class {
  plugin;
  app;
  toolbarEl = null;
  constructor(plugin) {
    this.plugin = plugin;
    this.app = plugin.app;
  }
  start() {
    this.plugin.registerEvent(this.app.workspace.on("active-leaf-change", () => this.refresh()));
    this.plugin.registerEvent(this.app.workspace.on("file-open", () => this.refresh()));
    this.plugin.registerEvent(this.app.workspace.on("layout-change", () => this.refresh()));
    this.app.workspace.onLayoutReady(() => this.refresh());
  }
  refresh() {
    this.removeToolbar();
    if (!this.plugin.settings.showTypstToolbar) {
      return;
    }
    const view = this.getActiveTypstView();
    if (!view) {
      return;
    }
    const contentEl = view.containerEl.querySelector(".view-content");
    if (!(contentEl instanceof HTMLElement)) {
      return;
    }
    this.toolbarEl = this.createToolbar();
    contentEl.prepend(this.toolbarEl);
  }
  removeToolbar() {
    this.toolbarEl?.remove();
    this.toolbarEl = null;
  }
  createToolbar() {
    const toolbarEl = document.createElement("div");
    toolbarEl.addClass("typst-inline-toolbar");
    let hasVisibleTool = false;
    for (const tool of TYPST_TOOLBAR_TOOLS) {
      if (!this.plugin.isTypstToolbarGroupEnabled(tool.group)) {
        continue;
      }
      if (tool.separatorBefore && hasVisibleTool) {
        toolbarEl.createDiv({ cls: "typst-inline-toolbar-separator" });
      }
      const buttonEl = toolbarEl.createEl("button", {
        cls: "clickable-icon typst-inline-toolbar-button",
        text: tool.label,
        attr: {
          "aria-label": tool.title,
          title: tool.title,
          type: "button"
        }
      });
      buttonEl.addEventListener("mousedown", (event) => event.preventDefault());
      buttonEl.addEventListener("click", () => this.applyTool(tool));
      hasVisibleTool = true;
    }
    return toolbarEl;
  }
  applyTool(tool) {
    const view = this.getActiveTypstView();
    if (!view) {
      new import_obsidian.Notice("Open a .typ or .typ.md file in source mode first.");
      return;
    }
    const editor = view.editor;
    if (tool.kind === "insert") {
      this.applyInsertTool(tool, editor);
    } else if (tool.kind === "line-prefix") {
      this.applyLinePrefixTool(tool, editor);
    } else {
      this.applyWrapTool(tool, editor);
    }
    editor.focus();
  }
  applyWrapTool(tool, editor) {
    const prefix = tool.prefix ?? "";
    const suffix = tool.suffix ?? "";
    const cursor = editor.getCursor("from");
    const startOffset = editor.posToOffset(cursor);
    const selection = editor.getSelection();
    editor.replaceSelection(`${prefix}${selection}${suffix}`);
    if (!selection || tool.cursorOffset !== void 0) {
      editor.setCursor(editor.offsetToPos(startOffset + (tool.cursorOffset ?? prefix.length)));
    }
  }
  applyInsertTool(tool, editor) {
    const cursor = editor.getCursor("from");
    const startOffset = editor.posToOffset(cursor);
    const text = tool.text ?? "";
    editor.replaceSelection(text);
    if (tool.cursorOffset !== void 0) {
      editor.setCursor(editor.offsetToPos(startOffset + tool.cursorOffset));
    }
  }
  applyLinePrefixTool(tool, editor) {
    const linePrefix = tool.linePrefix ?? "";
    const selection = editor.getSelection();
    if (selection) {
      editor.replaceSelection(prefixSelectedLines(selection, linePrefix));
      return;
    }
    const cursor = editor.getCursor("from");
    editor.replaceRange(linePrefix, { line: cursor.line, ch: 0 });
    editor.setCursor({ line: cursor.line, ch: cursor.ch + linePrefix.length });
  }
  getActiveTypstView() {
    const view = this.app.workspace.getActiveViewOfType(import_obsidian.MarkdownView);
    if (!view || view.getMode() !== "source" || !view.file || !isTypstSourcePath(view.file.path)) {
      return null;
    }
    return view;
  }
};
function prefixSelectedLines(text, prefix) {
  return text.split("\n").map((line) => line.length === 0 ? line : `${prefix}${line}`).join("\n");
}
var TypstBookPreviewView = class extends import_obsidian.ItemView {
  plugin;
  statusEl = null;
  errorEl = null;
  frameEl = null;
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
  }
  getViewType() {
    return VIEW_TYPE_TYPST_BOOK_PREVIEW;
  }
  getDisplayText() {
    return "Typst Book Preview";
  }
  getIcon() {
    return "book-open";
  }
  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass("typst-book-preview-view");
    const toolbarEl = container.createDiv({ cls: "typst-book-preview-toolbar" });
    toolbarEl.createDiv({
      cls: "typst-book-preview-title",
      text: "Typst Book Preview"
    });
    const compileButton = toolbarEl.createEl("button", {
      cls: "clickable-icon typst-book-preview-compile-button",
      attr: {
        "aria-label": "Compile Typst Book",
        title: "Compile Typst Book"
      }
    });
    compileButton.createSpan({ text: "Compile" });
    this.registerDomEvent(compileButton, "click", () => {
      void this.plugin.compile("manual");
    });
    this.statusEl = container.createDiv({ cls: "typst-book-preview-status" });
    this.errorEl = container.createDiv({ cls: "typst-book-preview-errors" });
    this.frameEl = container.createDiv({ cls: "typst-book-preview-frame" });
    this.render();
  }
  render() {
    if (!this.statusEl || !this.errorEl || !this.frameEl) {
      return;
    }
    const state = this.plugin.state;
    this.statusEl.setText(formatStatus(state));
    this.statusEl.toggleClass("is-compiling", state.status === "compiling");
    this.statusEl.toggleClass("is-error", state.status === "error");
    this.statusEl.toggleClass("is-success", state.status === "success");
    this.renderCompilerOutput(state);
    this.renderPdf(state);
  }
  renderCompilerOutput(state) {
    if (!this.errorEl) {
      return;
    }
    this.errorEl.empty();
    if (!state.errorText) {
      this.errorEl.hide();
      return;
    }
    this.errorEl.show();
    this.errorEl.toggleClass("is-error", state.status === "error");
    this.errorEl.toggleClass("is-output", state.status !== "error");
    const headerEl = this.errorEl.createDiv({ cls: "typst-book-preview-errors-header" });
    headerEl.createDiv({
      cls: "typst-book-preview-errors-heading",
      text: state.status === "error" ? "Compile problem" : "Compiler output"
    });
    const actionsEl = headerEl.createDiv({ cls: "typst-book-preview-error-actions" });
    this.createActionButton(actionsEl, "Compile again", () => {
      void this.plugin.compile("manual");
    });
    this.createActionButton(actionsEl, "Copy", () => {
      void copyToClipboard(this.plugin.diagnosticText());
    });
    this.createActionButton(actionsEl, "Use active file", () => {
      const activeFile = this.app.workspace.getActiveFile();
      if (!activeFile || !isTypstSourcePath(activeFile.path)) {
        new import_obsidian.Notice("Open a .typ or .typ.md file first.");
        return;
      }
      void this.plugin.setMainTypstPath(activeFile.path);
      new import_obsidian.Notice(`Typst Book Preview: main file set to ${activeFile.path}`);
    });
    this.createActionButton(actionsEl, "Settings", () => {
      openPluginSettings(this.app);
    });
    const summaryEl = this.errorEl.createDiv({ cls: "typst-book-preview-error-summary" });
    summaryEl.createDiv({ text: `Main file: ${this.plugin.getMainTypstPath()}` });
    summaryEl.createDiv({ text: `Output PDF: ${this.plugin.getOutputPdfPath()}` });
    summaryEl.createDiv({ text: `Typst command: ${this.plugin.getDisplayTypstCommand()}` });
    this.errorEl.createEl("pre", { text: state.errorText });
  }
  createActionButton(container, text, onClick) {
    const button = container.createEl("button", {
      cls: "typst-book-preview-error-button",
      text
    });
    this.registerDomEvent(button, "click", onClick);
  }
  renderPdf(state) {
    if (!this.frameEl) {
      return;
    }
    this.frameEl.empty();
    if (!state.pdfPath) {
      this.frameEl.createDiv({
        cls: "typst-book-preview-empty",
        text: `No PDF preview yet. Compile ${this.plugin.getMainTypstPath()} to create ${this.plugin.getOutputPdfPath()}.`
      });
      return;
    }
    const resourcePath = getPdfResourcePath(this.app, state.pdfPath);
    if (!resourcePath) {
      this.frameEl.createDiv({
        cls: "typst-book-preview-empty",
        text: `Compiled PDF was not found in the vault: ${state.pdfPath}`
      });
      return;
    }
    const separator = resourcePath.includes("?") ? "&" : "?";
    this.frameEl.createEl("iframe", {
      attr: {
        src: `${resourcePath}${separator}typst-book-preview=${state.updatedAt ?? Date.now()}`,
        title: "Typst PDF preview"
      }
    });
  }
};
var TypstBookPreviewSettingTab = class extends import_obsidian.PluginSettingTab {
  plugin;
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    new import_obsidian.Setting(containerEl).setName("Typst Book Preview").setHeading();
    new import_obsidian.Setting(containerEl).setName("Typst CLI command").setDesc("Command or absolute path to the local Typst CLI. Arguments are passed separately without a shell.").addText((text) => {
      text.setPlaceholder(DEFAULT_SETTINGS.typstCommand).setValue(this.plugin.settings.typstCommand).onChange(async (value) => {
        this.plugin.settings.typstCommand = value.trim() || DEFAULT_SETTINGS.typstCommand;
        await this.plugin.saveSettings();
      });
    });
    new import_obsidian.Setting(containerEl).setName("Main Typst file").setDesc("Vault-relative path to the book entry file. Use Choose file to search existing .typ and .typ.md files.").addText((text) => {
      text.setPlaceholder(DEFAULT_SETTINGS.mainTypstPath).setValue(this.plugin.settings.mainTypstPath).onChange(async (value) => {
        await this.plugin.setMainTypstPath(value.trim() || DEFAULT_SETTINGS.mainTypstPath);
      });
    }).addButton((button) => {
      button.setButtonText("Choose file").onClick(() => {
        new TypstSourceSuggestModal(this.app, async (file) => {
          await this.plugin.setMainTypstPath(file.path);
          this.display();
          new import_obsidian.Notice(`Typst Book Preview: main file set to ${file.path}`);
        }).open();
      });
    });
    new import_obsidian.Setting(containerEl).setName("Typst styling toolbar").setDesc("Show formatting buttons above source-mode .typ and .typ.md notes.").addToggle((toggle) => {
      toggle.setValue(this.plugin.settings.showTypstToolbar).onChange(async (value) => {
        this.plugin.settings.showTypstToolbar = value;
        await this.plugin.saveSettings();
        this.plugin.refreshTypstToolbar();
      });
    });
    new import_obsidian.Setting(containerEl).setName("Typst toolbar groups").setHeading();
    for (const group of TYPST_TOOLBAR_GROUP_OPTIONS) {
      new import_obsidian.Setting(containerEl).setName(group.name).setDesc(group.description).addToggle((toggle) => {
        toggle.setValue(this.plugin.isTypstToolbarGroupEnabled(group.id)).onChange(async (value) => {
          this.plugin.settings.toolbarGroups[group.id] = value;
          await this.plugin.saveSettings();
          this.plugin.refreshTypstToolbar();
        });
      });
    }
    new import_obsidian.Setting(containerEl).setName("Preview pane").setDesc("Open the PDF preview pane and compile the configured book.").addButton((button) => {
      button.setButtonText("Open preview").onClick(() => {
        void this.plugin.activateView();
      });
    }).addButton((button) => {
      button.setButtonText("Use active file").onClick(() => {
        const activeFile = this.app.workspace.getActiveFile();
        if (!activeFile || !isTypstSourcePath(activeFile.path)) {
          new import_obsidian.Notice("Open a .typ or .typ.md file first.");
          return;
        }
        void this.plugin.setMainTypstPath(activeFile.path);
      });
    }).addButton((button) => {
      button.setButtonText("Compile now").setCta().onClick(() => {
        void this.plugin.compile("manual");
      });
    });
  }
};
var TypstSourceSuggestModal = class extends import_obsidian.SuggestModal {
  onChooseFile;
  constructor(app, onChooseFile) {
    super(app);
    this.onChooseFile = onChooseFile;
    this.setPlaceholder("Search .typ or .typ.md files");
  }
  getSuggestions(query) {
    const normalizedQuery = query.trim().toLowerCase();
    return this.app.vault.getFiles().filter((file) => {
      return isTypstSourcePath(file.path) && file.path.toLowerCase().includes(normalizedQuery);
    }).sort((left, right) => left.path.localeCompare(right.path)).slice(0, 50);
  }
  renderSuggestion(file, el) {
    el.createDiv({ cls: "suggestion-title", text: file.basename });
    el.createDiv({ cls: "suggestion-note", text: file.path });
  }
  onChooseSuggestion(file, _event) {
    void this.onChooseFile(file);
  }
};
function execFilePromise(command, args, options) {
  return new Promise((resolve2, reject) => {
    (0, import_child_process.execFile)(command, args, options, (error, stdout, stderr) => {
      if (error) {
        const execError = error;
        execError.stdout = stdout;
        execError.stderr = stderr;
        reject(execError);
        return;
      }
      resolve2({
        stdout: stdout ?? "",
        stderr: stderr ?? ""
      });
    });
  });
}
function compilerErrorToString(error) {
  if (typeof error !== "object" || error === null) {
    return errorToString(error);
  }
  const execError = error;
  const compilerOutput = [execError.stderr, execError.stdout].filter(Boolean).join("\n").trim();
  if (compilerOutput) {
    return compilerOutput;
  }
  return execError.message || "Typst failed without compiler output.";
}
function errorToString(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}
function formatStatus(state) {
  const suffix = state.updatedAt ? ` (${new Date(state.updatedAt).toLocaleTimeString()})` : "";
  return `${state.message}${suffix}`;
}
function isTypstSourcePath(vaultPath) {
  return /\.typ(?:\.md)?$/i.test(vaultPath);
}
function isImageAssetPath(vaultPath) {
  const extension = vaultPath.split(".").pop()?.toLowerCase() ?? "";
  return IMAGE_EXTENSIONS.has(extension);
}
function getOutputPdfPath(inputVaultPath) {
  return inputVaultPath.replace(/\.typ(?:\.md)?$/i, ".pdf");
}
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    new import_obsidian.Notice("Typst Book Preview: copied diagnostics.");
  } catch (error) {
    new import_obsidian.Notice(`Typst Book Preview: copy failed: ${errorToString(error)}`);
  }
}
function openPluginSettings(app) {
  const setting = app.setting;
  if (!setting) {
    new import_obsidian.Notice("Open Settings > Typst Book Preview.");
    return;
  }
  setting.open();
  setting.openTabById("typst-book-preview");
}
function getVaultBasePath(app) {
  const adapter = app.vault.adapter;
  const basePath = adapter.getBasePath?.();
  if (!basePath) {
    throw new Error("Typst Book Preview requires the desktop file-system vault adapter.");
  }
  return basePath;
}
function getPdfResourcePath(app, vaultPath) {
  const adapter = app.vault.adapter;
  if (adapter.getResourcePath) {
    return adapter.getResourcePath(vaultPath);
  }
  const file = app.vault.getAbstractFileByPath(vaultPath);
  return file instanceof import_obsidian.TFile ? app.vault.getResourcePath(file) : null;
}
function resolveInsideVault(vaultBasePath, vaultPath) {
  const vaultRoot = path.resolve(vaultBasePath);
  const resolvedPath = path.resolve(vaultRoot, vaultPath);
  if (resolvedPath !== vaultRoot && !resolvedPath.startsWith(`${vaultRoot}${path.sep}`)) {
    throw new Error(`Path escapes the vault: ${vaultPath}`);
  }
  return resolvedPath;
}
function validateVaultPath(vaultPath, label) {
  if (!vaultPath) {
    throw new Error(`${label} is required.`);
  }
  if (path.isAbsolute(vaultPath) || vaultPath === "." || vaultPath === ".." || vaultPath.startsWith("../") || vaultPath.includes("/../")) {
    throw new Error(`${label} must be a vault-relative path.`);
  }
}

/* nosourcemap */