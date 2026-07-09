const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, LevelFormat, TabStopType,
  TabStopPosition, PageBreak
} = require('docx');
const fs = require('fs');
const path = require('path');

// ─── Colour palette ───────────────────────────────────────────
const BLU  = "1F3864";  // dark navy (headings)
const LBL  = "2E75B6";  // medium blue
const LBLT = "D6E4F0";  // light blue fill (table header)
const GRY  = "F2F7FB";  // very light blue-grey (alt row)
const WHT  = "FFFFFF";
const BLK  = "000000";
const DGY  = "404040";  // dark grey body text

// ─── Helper: thin border ─────────────────────────────────────
const thinBorder = { style: BorderStyle.SINGLE, size: 6, color: "AACCE0" };
const cellBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };

// ─── Helper: standard body text ─────────────────────────────
const body = (text, opts = {}) => new Paragraph({
  spacing: { after: 160, before: 0 },
  children: [new TextRun({ text, font: "Arial", size: 22, color: DGY, ...opts })]
});

const bodyBold = (text) => new Paragraph({
  spacing: { after: 120, before: 120 },
  children: [new TextRun({ text, font: "Arial", size: 22, color: BLU, bold: true })]
});

const spacer = (pts = 120) => new Paragraph({ spacing: { before: pts, after: 0 }, children: [] });

// ─── Helper: code-style paragraph ────────────────────────────
const code = (text) => new Paragraph({
  spacing: { after: 40, before: 40 },
  indent: { left: 360 },
  shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
  children: [new TextRun({ text, font: "Courier New", size: 18, color: "003366" })]
});

// ─── Helper: bullet item ─────────────────────────────────────
const bullet = (text, bold = "") => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 100 },
  children: [
    ...(bold ? [new TextRun({ text: bold + " ", font: "Arial", size: 22, bold: true, color: BLU })] : []),
    new TextRun({ text, font: "Arial", size: 22, color: DGY })
  ]
});

// ─── Helper: numbered item ───────────────────────────────────
const numbered = (text) => new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  spacing: { after: 100 },
  children: [new TextRun({ text, font: "Arial", size: 22, color: DGY })]
});

// ─── Helper: heading 1 ───────────────────────────────────────
const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 360, after: 160 },
  children: [new TextRun({ text, font: "Arial", size: 32, bold: true, color: BLU })]
});

// ─── Helper: heading 2 ───────────────────────────────────────
const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 240, after: 120 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LBL, space: 1 } },
  children: [new TextRun({ text, font: "Arial", size: 26, bold: true, color: LBL })]
});

// ─── Helper: heading 3 ───────────────────────────────────────
const h3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 180, after: 80 },
  children: [new TextRun({ text, font: "Arial", size: 23, bold: true, color: "3A6EA5" })]
});

// ─── Helper: table header cell ───────────────────────────────
const thCell = (text, width) => new TableCell({
  borders: cellBorders,
  width: { size: width, type: WidthType.DXA },
  shading: { fill: LBLT, type: ShadingType.CLEAR },
  margins: { top: 80, bottom: 80, left: 140, right: 140 },
  verticalAlign: VerticalAlign.CENTER,
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text, font: "Arial", size: 20, bold: true, color: BLU })]
  })]
});

// ─── Helper: table data cell ─────────────────────────────────
const tdCell = (text, width, fill = WHT, bold = false, align = AlignmentType.LEFT) =>
  new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 140, right: 140 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text, font: "Arial", size: 20, bold, color: DGY })]
    })]
  });

// ─── Lab Coverage Table ───────────────────────────────────────
const labTableRows = [
  ["Lab 01", "INT 10h / INT 16h / INT 21h", "BIOS video & keyboard; DOS output; program exit (4Ch)"],
  ["Lab 02", "Register Architecture", "AX, BX, CX, DX and sub-registers (AH/AL); CX as loop counter"],
  ["Lab 03", "Data Definitions", "DB / DW declarations; '$'-terminated string messages"],
  ["Lab 04", "Addressing Modes", "Immediate, Register, Direct, and Indexed (base+SI) addressing"],
  ["Lab 05", "Conditional Jumps", "CMP with JE, JNE, JG, JL, JBE, JAE, JZ, JNZ, JGE"],
  ["Lab 06", "LOOP Instruction", "Balloon/bullet tick counters; nested NOP delay loops"],
  ["Lab 07", "Arithmetic Instructions", "ADD, SUB, INC, DEC, DIV (decimal print); score/lives update"],
  ["Lab 08", "Parallel Byte Arrays", "bal_col[], bal_row[], bal_live[] indexed with SI register"],
  ["Lab 09", "Logical Instructions", "AND (colour/column masking), XOR, NEG, TEST (sign check)"],
  ["Lab 10", "Shift Instructions", "SHL for pseudo-random column reset; SHR available"],
  ["Lab 11", "Rotate Instructions", "ROL anim byte 1-bit/tick; balloon colour alternation"],
  ["Lab 12", "Modular Procedures", "GOTOXY, PUTCHAT, CLR_SCR, DRAW_*, ERASE_*, CHECK_HIT, etc."],
  ["Lab 13", "Stack Operations", "PUSH/POP every register on entry/exit of every procedure"],
];

function makeLabTable() {
  const cols = [900, 2600, 5860];
  const rows = [
    new TableRow({
      tableHeader: true,
      children: [thCell("Lab", cols[0]), thCell("Concept", cols[1]), thCell("Implementation in BALLOON POP!", cols[2])]
    }),
    ...labTableRows.map((r, i) => new TableRow({
      children: [
        tdCell(r[0], cols[0], i % 2 === 0 ? WHT : GRY, true, AlignmentType.CENTER),
        tdCell(r[1], cols[1], i % 2 === 0 ? WHT : GRY, true),
        tdCell(r[2], cols[2], i % 2 === 0 ? WHT : GRY),
      ]
    }))
  ];
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: cols,
    rows
  });
}

// ─── Procedure Summary Table ─────────────────────────────────
const procData = [
  ["GOTOXY", "DH=row, DL=col", "—", "Moves text cursor using INT 10h AH=02h"],
  ["PUTCHAT", "AL=char, BL=colour, DH/DL=pos", "—", "Draws a coloured character at a screen position"],
  ["CLR_SCR", "—", "—", "Resets video to mode 3 (80×25 colour text)"],
  ["DRAW_FRAME", "—", "—", "Renders top/bottom borders and the control-key hint row"],
  ["DRAW_HUD", "—", "—", "Refreshes the score (DW) and lives (DB) display on row 0"],
  ["DRAW_CANNON", "—", "—", "Draws the 3-char '[^]' sprite at gun_col on CANNON_ROW"],
  ["ERASE_CANNON", "—", "—", "Overwrites 3 spaces at the cannon's current position"],
  ["DRAW_BAL", "SI=balloon index", "—", "Draws '(*) ' sprite; picks colour from ROL animation byte"],
  ["ERASE_BAL", "SI=balloon index", "—", "Overwrites 3 spaces at the balloon's current position"],
  ["DRAW_BULLET", "—", "—", "Draws '|' at blt_row, blt_col with yellow attribute"],
  ["ERASE_BULLET", "—", "—", "Draws a space at the bullet's current position"],
  ["CHECK_HIT", "—", "—", "Loops all balloons; tests row match and |col| ≤ 3 proximity"],
  ["DELAY_SHORT", "—", "—", "Burns 128 NOP cycles for frame-rate pacing"],
  ["PRINT_DEC", "AX=value", "—", "Converts 16-bit integer to ASCII decimal via repeated DIV"],
];

function makeProcTable() {
  const cols = [1800, 2400, 720, 4440];
  const rows = [
    new TableRow({
      tableHeader: true,
      children: [thCell("Procedure", cols[0]), thCell("Inputs", cols[1]), thCell("Output", cols[2]), thCell("Description", cols[3])]
    }),
    ...procData.map((r, i) => new TableRow({
      children: [
        tdCell(r[0], cols[0], i % 2 === 0 ? WHT : GRY, true),
        tdCell(r[1], cols[1], i % 2 === 0 ? WHT : GRY),
        tdCell(r[2], cols[2], i % 2 === 0 ? WHT : GRY, false, AlignmentType.CENTER),
        tdCell(r[3], cols[3], i % 2 === 0 ? WHT : GRY),
      ]
    }))
  ];
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: cols,
    rows
  });
}

// ─── Data Variables Table ─────────────────────────────────────
const varData = [
  ["bal_col", "DB × 5", "Array", "Starting/current X-column of each balloon"],
  ["bal_row", "DB × 5", "Array", "Starting/current Y-row of each balloon"],
  ["bal_live", "DB × 5", "Array", "1 = alive; 0 = popped (indexed by SI)"],
  ["gun_col", "DB", "Variable", "Current column of the player's cannon"],
  ["blt_col / blt_row", "DB", "Variable", "Current column and row of the in-flight bullet"],
  ["blt_fly", "DB", "Flag", "0 = no bullet active; 1 = bullet in flight"],
  ["score", "DW", "Variable", "Player score (word; incremented +10 per pop)"],
  ["lives", "DB", "Variable", "Remaining lives (3 to 0); decremented on balloon escape"],
  ["n_pop", "DB", "Counter", "Number of balloons popped; win condition when = NUM_BAL"],
  ["anim", "DB", "Bit Pattern", "Rotated 1-bit left per tick; bit-0 selects balloon colour"],
  ["bal_cnt / blt_cnt", "DW", "Counter", "Tick counters controlling balloon and bullet speed"],
  ["ended", "DB", "Flag", "Set to 1 when lives reach 0; triggers GAME OVER state"],
];

function makeVarTable() {
  const cols = [2000, 900, 1500, 4960];
  const rows = [
    new TableRow({
      tableHeader: true,
      children: [thCell("Variable", cols[0]), thCell("Type", cols[1]), thCell("Category", cols[2]), thCell("Purpose", cols[3])]
    }),
    ...varData.map((r, i) => new TableRow({
      children: [
        tdCell(r[0], cols[0], i % 2 === 0 ? WHT : GRY, true),
        tdCell(r[1], cols[1], i % 2 === 0 ? WHT : GRY, false, AlignmentType.CENTER),
        tdCell(r[2], cols[2], i % 2 === 0 ? WHT : GRY),
        tdCell(r[3], cols[3], i % 2 === 0 ? WHT : GRY),
      ]
    }))
  ];
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: cols,
    rows
  });
}

// ─── Title Page ───────────────────────────────────────────────
function makeTitlePage() {
  return [
    spacer(1200),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [new TextRun({ text: "BAHRIA UNIVERSITY KARACHI CAMPUS", font: "Arial", size: 24, bold: true, color: BLU })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 400 },
      children: [new TextRun({ text: "Department of Computer Science", font: "Arial", size: 22, color: DGY })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: LBL, space: 6 } },
      children: [new TextRun({ text: "BALLOON POP!", font: "Arial", size: 60, bold: true, color: BLU })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [new TextRun({ text: "An 8086 Assembly Language Game", font: "Arial", size: 28, color: LBL, italics: true })]
    }),
    spacer(320),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [new TextRun({ text: "Project Report", font: "Arial", size: 26, bold: true, color: DGY })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [new TextRun({ text: "Computer Organization & Assembly Language (COAL) — CEL-323", font: "Arial", size: 22, color: DGY })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [new TextRun({ text: "4th Semester  |  Spring 2026", font: "Arial", size: 22, color: DGY })]
    }),
    spacer(600),
    // divider
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LBLT, space: 2 } },
      children: []
    }),
    spacer(160),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [new TextRun({ text: "Submitted By:", font: "Arial", size: 22, bold: true, color: BLU })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [new TextRun({ text: "[Student Name]  |  [Roll Number]", font: "Arial", size: 22, color: DGY })]
    }),
    spacer(120),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [new TextRun({ text: "Submitted To:", font: "Arial", size: 22, bold: true, color: BLU })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [new TextRun({ text: "[Instructor Name]", font: "Arial", size: 22, color: DGY })]
    }),
    spacer(120),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [new TextRun({ text: "Submission Date:", font: "Arial", size: 22, bold: true, color: BLU })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [new TextRun({ text: "May 2026", font: "Arial", size: 22, color: DGY })]
    }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// ────────────────────────────────────────────────────────────────────────────
//  BUILD DOCUMENT
// ────────────────────────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      },
      {
        reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22, color: DGY } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: BLU },
        paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: LBL },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: "Arial", color: "3A6EA5" },
        paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1260, bottom: 1440, left: 1260 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LBL, space: 1 } },
            spacing: { after: 60 },
            children: [
              new TextRun({ text: "BALLOON POP! — COAL CEL-323 Project Report", font: "Arial", size: 18, color: LBL })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 6, color: LBL, space: 1 } },
            spacing: { before: 60 },
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            children: [
              new TextRun({ text: "Bahria University Karachi Campus  |  Spring 2026", font: "Arial", size: 18, color: "888888" }),
              new TextRun({ text: "\tPage ", font: "Arial", size: 18, color: "888888" }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "888888" }),
              new TextRun({ text: " of ", font: "Arial", size: 18, color: "888888" }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: "888888" }),
            ]
          })
        ]
      })
    },
    children: [

      // ═══════════════ TITLE PAGE ═══════════════
      ...makeTitlePage(),

      // ═══════════════ 1. INTRODUCTION ═══════════
      h1("1. Introduction"),
      body("BALLOON POP! is a fully-functional arcade-style game written in 8086 Assembly Language and designed to run on the EMU8086 emulator. The project was developed as the capstone deliverable for Computer Organization & Assembly Language (COAL) — CEL-323 at Bahria University Karachi Campus."),
      spacer(80),
      body("The core objective of the game is simple: the player controls a ground-based cannon and must shoot down five descending balloons before they reach the bottom of the screen. Every balloon that escapes costs the player one of their three lives. Each successful pop adds 10 points to the score. The game ends either when all lives are lost (GAME OVER) or when all five balloons have been popped (YOU WIN!)."),
      spacer(80),
      body("From an academic standpoint, the project serves as a practical demonstration of every concept covered in Labs 01 through 13. Rather than treating each lab in isolation, the game integrates all thirteen topics into a single, cohesive, real-time application."),

      spacer(160),
      h1("2. Objectives"),
      body("The project was designed to achieve the following objectives:"),
      bullet("Demonstrate mastery of 8086 assembly programming constructs as taught across thirteen laboratory sessions.", "Academic:"),
      bullet("Design and implement a real-time game loop in a resource-constrained text-mode environment (80×25 colour terminal).", "Technical:"),
      bullet("Apply modular procedure-based architecture to keep the codebase readable, testable, and debuggable.", "Software Engineering:"),
      bullet("Use BIOS (INT 10h) and DOS (INT 21h) interrupts for all input/output, without any high-level language support.", "Low-Level I/O:"),
      bullet("Demonstrate correct stack discipline (PUSH/POP) across all fourteen procedures.", "Stack Management:"),
      bullet("Provide an engaging, playable game that clearly showcases the power of low-level programming.", "Game Design:"),

      spacer(160),
      h1("3. Game Overview"),

      h2("3.1 Gameplay"),
      body("The player controls a three-character cannon sprite [^] that sits on a fixed row at the bottom of the screen. Five balloons (*) start at staggered positions near the top and descend one row at a time at a configurable speed. The player presses A/D to slide the cannon left or right, and SPACE to fire a bullet upward. A bullet that passes within three columns of a balloon's centre counts as a hit."),

      h2("3.2 Screen Layout"),
      body("The display is divided into clear functional zones:"),

      spacer(60),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [1800, 7560],
        rows: [
          new TableRow({ children: [thCell("Row(s)", 1800), thCell("Content", 7560)] }),
          ...([
            ["Row 0", "HUD — live score and lives counter"],
            ["Row 1", "Top border (= characters)"],
            ["Rows 2 – 20", "Active game arena — balloons and bullet travel here"],
            ["Row 21", "Escape boundary — balloon reaching this row costs a life"],
            ["Row 22", "Bottom border; cannon [^] occupies this row"],
            ["Row 23", "Empty buffer"],
            ["Row 24", "Control-key reference bar"],
          ].map((r, i) => new TableRow({
            children: [
              tdCell(r[0], 1800, i % 2 === 0 ? WHT : GRY, true, AlignmentType.CENTER),
              tdCell(r[1], 7560, i % 2 === 0 ? WHT : GRY),
            ]
          })))
        ]
      }),

      spacer(160),
      h2("3.3 Controls"),
      bullet("Move cannon two columns to the left", "[A] / [a] —"),
      bullet("Move cannon two columns to the right", "[D] / [d] —"),
      bullet("Fire a bullet (only one bullet in the air at a time)", "[SPACE] —"),
      bullet("Immediately quit and return to DOS", "[Q] / [q] —"),

      spacer(160),
      h2("3.4 Scoring & Win / Loss Conditions"),
      bullet("Each balloon successfully shot: +10 points"),
      bullet("Each balloon that escapes the bottom boundary: −1 life"),
      bullet("Win condition: all 5 balloons popped (any score)"),
      bullet("Loss condition: lives reach 0 before all balloons are cleared"),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 4. LAB CONCEPTS ════════════
      h1("4. Lab Concepts & Implementation"),
      body("The table below maps every laboratory topic (Labs 01–13) to its concrete usage inside BALLOON POP!. Every concept appears in the production game code — there are no placeholder or unused sections."),
      spacer(120),
      makeLabTable(),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 5. ARCHITECTURE ════════════
      h1("5. Program Architecture"),

      h2("5.1 Memory Model & Segment Setup"),
      body("The program uses the SMALL memory model (.MODEL SMALL), meaning code and data each fit within a single 64 KB segment. The stack is allocated at 512 bytes (.STACK 200h), which is sufficient for the deepest call chain of five nested PUSH operations. The data segment register DS is initialised at the start of MAIN using:"),
      spacer(60),
      code("MOV  AX, @DATA"),
      code("MOV  DS, AX"),
      spacer(60),
      body("All variable and array accesses throughout the program use DS-relative addressing."),

      spacer(160),
      h2("5.2 Game Loop Structure"),
      body("The main game loop (GAME_LOOP) runs continuously and is structured into three distinct phases per iteration:"),
      numbered("Keyboard Input (Step 1) — INT 16h AH=01h polls for a keypress without blocking. Detected keys dispatch to movement or fire handlers."),
      numbered("Bullet Update (Step 2) — A tick counter (blt_cnt) throttles bullet movement. When the threshold (BUL_TICKS = 80) is reached, the bullet is erased, moved up one row, redrawn, and collision-checked."),
      numbered("Balloon Update (Step 3) — A second tick counter (bal_cnt) throttles balloon descent. When BAL_TICKS (1500) is reached, all live balloons are erased, moved down one row, and redrawn. Escaped balloons trigger a life deduction and column reset."),
      spacer(80),
      body("After all three phases, the loop checks the ended flag (set to avoid a long jump from inside the balloon loop) and the n_pop counter. If all five balloons are popped, the win screen is shown; if ended = 1, the game-over screen is shown; otherwise execution jumps back to GAME_LOOP."),

      spacer(160),
      h2("5.3 Procedure Inventory"),
      body("The program is divided into fourteen modular procedures. Every procedure follows strict stack discipline: all registers used are saved with PUSH on entry and restored with POP on exit."),
      spacer(120),
      makeProcTable(),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 6. DATA SEGMENT ════════════
      h1("6. Data Segment Design"),

      h2("6.1 Variable & Array Reference"),
      body("The .DATA segment holds all game state. Variables are declared as DB (1 byte) or DW (2 bytes/word) following Lab 03 conventions. The three balloon arrays are the most critical data structures — they are parallel byte arrays accessed with a common SI index, a pattern taught in Lab 08."),
      spacer(120),
      makeVarTable(),

      spacer(160),
      h2("6.2 Balloon Array Design (Lab 08)"),
      body("Three parallel DB arrays of length NUM_BAL (5) hold the complete state of all balloons:"),
      spacer(60),
      code("bal_col  DB   5, 20, 37, 54, 69   ; X-column (staggered to avoid overlap)"),
      code("bal_row  DB   2,  4,  2,  5,  3   ; Y-row    (staggered start heights)"),
      code("bal_live DB   1,  1,  1,  1,  1   ; alive flag (1 = active, 0 = popped)"),
      spacer(60),
      body("The SI register serves as the common array index. All three arrays are accessed with the same SI value in every loop iteration (e.g. bal_col[SI], bal_row[SI], bal_live[SI]), implementing the parallel-array pattern from Lab 08."),

      spacer(160),
      h2("6.3 Animation Byte (Lab 11)"),
      body("A single byte variable 'anim' is rotated one bit left (ROL) on every game tick:"),
      spacer(60),
      code("ROL  anim, 1             ; rotate left — cycles bit pattern every 8 ticks"),
      spacer(60),
      body("In DRAW_BAL, bit-0 of anim is isolated with AND AL, 01h (Lab 09). If the result is 1, balloons are drawn in bright red (COL_BAL1 = 0Ch); if 0, they are drawn in bright cyan (COL_BAL2 = 0Bh). This creates a smooth two-colour alternating animation without any conditional branches that reference external timers."),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 7. KEY PROCEDURES ══════════
      h1("7. Key Procedure Deep-Dives"),

      h2("7.1 CHECK_HIT — Collision Detection"),
      body("CHECK_HIT is the most algorithmically complex procedure in the project. It implements axis-aligned bounding-box (AABB) collision detection entirely in assembly:"),
      numbered("Loop over all NUM_BAL balloons using the LOOP instruction (Lab 06) with SI as the index."),
      numbered("Skip any balloon where bal_live[SI] = 0 (already popped)."),
      numbered("Compare blt_row with bal_row[SI] using CMP / JNE (Lab 05) — exact row match required."),
      numbered("Compute |blt_col − bal_col[SI]| using SUB, then TEST the sign bit (Lab 09). If negative, negate with NEG (Lab 09) to get the absolute distance."),
      numbered("Compare the distance with 3 using CMP / JG (Lab 05). A distance of 3 or less is a hit."),
      numbered("On a hit: erase the balloon, mark bal_live[SI] = 0, stop the bullet, add 10 to score (Lab 07 ADD), increment n_pop, display the 'POP' flash, pause with a LOOP-driven delay (Lab 06), then erase the flash and refresh the HUD."),
      spacer(80),
      body("The procedure correctly handles a one-bullet-one-hit rule: after the first hit is processed, execution jumps to CH_DONE, bypassing the rest of the balloon array."),

      spacer(160),
      h2("7.2 PRINT_DEC — Decimal Number Output"),
      body("The 8086 has no built-in decimal-output instruction. PRINT_DEC converts a 16-bit integer in AX to ASCII characters using a repeated-division algorithm:"),
      numbered("Divide AX by 10. The remainder (DX) is the least-significant digit."),
      numbered("PUSH the remainder digit onto the stack (Lab 13). Increment the digit count in CX (Lab 07)."),
      numbered("Repeat until the quotient (AX) is 0."),
      numbered("POP digits from the stack. Because the stack is LIFO, digits come out most-significant-first, which is the correct print order."),
      numbered("Add '0' to each digit (ASCII offset) and output via INT 21h AH=02h (Lab 01)."),
      spacer(80),
      body("This elegant use of the stack (Lab 13) as an implicit digit-reversal buffer is a classic assembly pattern."),

      spacer(160),
      h2("7.3 Pseudo-Random Column Reset (Labs 09 & 10)"),
      body("When a balloon escapes the bottom, it must reappear at a plausible but different column so the game doesn't become predictable. The game achieves this without a hardware random-number generator by exploiting the current column value:"),
      spacer(60),
      code("MOV  AL, bal_col[SI]"),
      code("SHL  AL, 1               ; Lab 10: multiply column by 2"),
      code("AND  AL, 3Fh             ; Lab 09: mask to range 0..63"),
      code("ADD  AL, 5               ; Lab 07: ensure minimum left margin"),
      spacer(60),
      body("SHL (Lab 10) doubles the column; AND with 3Fh (Lab 09) wraps it into the 0–63 range. Adding 5 prevents the balloon from spawning too close to the left border. A boundary check then clamps the result to a maximum of 74 (leaving room for the 3-character sprite before column 79)."),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 8. CONSTANTS ═══════════════
      h1("8. EQU Constants & Tuning"),
      body("All magic numbers are replaced with named EQU constants defined at the top of the source file, following good assembly style:"),
      spacer(80),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2200, 1200, 5960],
        rows: [
          new TableRow({ children: [thCell("Constant", 2200), thCell("Value", 1200), thCell("Purpose", 5960)] }),
          ...([
            ["GAME_TOP", "2", "First row where balloons appear"],
            ["GAME_BOT", "21", "Row at which a balloon is considered escaped"],
            ["CANNON_ROW", "22", "Row on which the player cannon sits"],
            ["NUM_BAL", "5", "Total number of balloons in the game"],
            ["BAL_TICKS", "1500", "Game ticks between balloon row increments (speed control)"],
            ["BUL_TICKS", "80", "Game ticks between bullet row decrements (speed control)"],
            ["COL_BAL1", "0Ch", "Bright red colour attribute for balloon (animation frame A)"],
            ["COL_BAL2", "0Bh", "Bright cyan colour attribute for balloon (animation frame B)"],
            ["COL_CANNON", "0Ah", "Bright green colour attribute for the cannon sprite"],
            ["COL_BULLET", "0Eh", "Yellow colour attribute for the bullet"],
            ["COL_POP", "0Fh", "Bright white colour attribute for the POP! flash text"],
            ["COL_ERASE", "00h", "Black-on-black attribute used to erase any character"],
          ].map((r, i) => new TableRow({
            children: [
              tdCell(r[0], 2200, i % 2 === 0 ? WHT : GRY, true),
              tdCell(r[1], 1200, i % 2 === 0 ? WHT : GRY, false, AlignmentType.CENTER),
              tdCell(r[2], 5960, i % 2 === 0 ? WHT : GRY),
            ]
          })))
        ]
      }),
      spacer(120),
      body("BAL_TICKS and BUL_TICKS are the primary difficulty-tuning levers. Decreasing BAL_TICKS makes balloons fall faster; decreasing BUL_TICKS makes the bullet travel faster. For best results in EMU8086, set the emulator speed to Maximum (Emulator → Set Speed → Maximum)."),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 9. INTERRUPT SERVICES ══════
      h1("9. Interrupt Services Used"),

      h2("9.1 INT 10h — BIOS Video Services"),
      bullet("AH=00h — Set video mode 3 (80×25 16-colour text). Called at start-up and on screen clear."),
      bullet("AH=01h — Set cursor shape. Used to hide (CX=2000h) and restore (CX=0607h) the text cursor."),
      bullet("AH=02h — Set cursor position. Called inside GOTOXY with BH=0 (page 0), DH=row, DL=column."),
      bullet("AH=09h — Write character with colour attribute. Called inside PUTCHAT to draw sprites; also called directly for multi-character sprite drawing (CX = repeat count)."),

      spacer(120),
      h2("9.2 INT 16h — BIOS Keyboard Services"),
      bullet("AH=01h — Poll keyboard (non-blocking). Returns ZF=1 if no key waiting, ZF=0 if a key is ready. This is the backbone of the non-blocking input loop."),
      bullet("AH=00h — Read key from buffer. Clears the key and returns ASCII code in AL."),

      spacer(120),
      h2("9.3 INT 21h — DOS Services"),
      bullet("AH=02h — Output a single character in DL to stdout. Used by PRINT_DEC for digit output."),
      bullet("AH=09h — Output a '$'-terminated string at DS:DX. Used for HUD labels, borders, controls, and end-game messages."),
      bullet("AH=4Ch — Terminate program with return code in AL. Called as MOV AX, 4C00h / INT 21h to cleanly exit to DOS."),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 10. GAME STATES ════════════
      h1("10. Game State Machine"),
      body("The program flows through a linear sequence of states:"),
      spacer(100),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2400, 6960],
        rows: [
          new TableRow({ children: [thCell("State", 2400), thCell("Description & Transition", 6960)] }),
          ...([
            ["INIT", "Sets video mode, hides cursor, draws static frame (borders + controls), draws HUD, draws cannon, draws all five starting balloons. Transitions immediately to GAME_LOOP."],
            ["GAME_LOOP", "Runs indefinitely. Each iteration: (1) reads input, (2) moves bullet, (3) moves balloons. Transitions to SHOW_GAME_OVER if ended=1, or SHOW_WIN if n_pop=NUM_BAL, or Q key pressed triggers DO_QUIT."],
            ["SHOW_GAME_OVER", "Clears screen, prints final score, waits for a keypress, then falls through to DO_QUIT."],
            ["SHOW_WIN", "Clears screen, prints winning score, waits for a keypress, then falls through to DO_QUIT."],
            ["DO_QUIT", "Restores cursor shape, clears screen, executes INT 21h AH=4Ch to return to DOS."],
          ].map((r, i) => new TableRow({
            children: [
              tdCell(r[0], 2400, i % 2 === 0 ? WHT : GRY, true, AlignmentType.CENTER),
              tdCell(r[1], 6960, i % 2 === 0 ? WHT : GRY),
            ]
          })))
        ]
      }),
      spacer(120),
      body("The ended flag is used deliberately to avoid a long conditional jump from deep inside the balloon update loop. The loop sets ended=1 and continues normally to clean up its stack (POP CX / POP SI) before GAME_LOOP checks the flag and branches to the game-over handler."),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 11. TESTING ═════════════════
      h1("11. Testing & Validation"),

      h2("11.1 Test Cases"),
      spacer(80),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3600, 2880, 2880],
        rows: [
          new TableRow({ children: [thCell("Test Scenario", 3600), thCell("Expected Result", 2880), thCell("Observed Result", 2880)] }),
          ...([
            ["Press [A] when cannon is at leftmost boundary (col ≤ 3)", "Cannon does not move; no graphical corruption", "Pass"],
            ["Press [D] when cannon is at rightmost boundary (col ≥ 74)", "Cannon does not move; no graphical corruption", "Pass"],
            ["Press [SPACE] twice without waiting for first bullet to finish", "Second fire ignored; only one bullet active", "Pass"],
            ["Bullet travels to top of screen without hitting any balloon", "Bullet erased; blt_fly reset to 0", "Pass"],
            ["Bullet column within 3 of a balloon's column on same row", "Balloon erased, 'POP' displayed, score +10, n_pop++", "Pass"],
            ["Bullet column more than 3 from all balloons on same row", "Bullet continues upward; no hit registered", "Pass"],
            ["Balloon reaches row GAME_BOT (21)", "Life decremented, balloon resets to row 2 with new column", "Pass"],
            ["Lives reduced to 0", "ended=1 set; GAME OVER screen displayed after loop completes", "Pass"],
            ["All 5 balloons popped (n_pop = 5)", "YOU WIN! screen displayed immediately", "Pass"],
            ["Press [Q] during gameplay", "Cursor restored, screen cleared, return to DOS", "Pass"],
            ["Run with EMU8086 at maximum speed", "All animations and movement render correctly", "Pass"],
          ].map((r, i) => new TableRow({
            children: [
              tdCell(r[0], 3600, i % 2 === 0 ? WHT : GRY),
              tdCell(r[1], 2880, i % 2 === 0 ? WHT : GRY),
              tdCell(r[2], 2880, i % 2 === 0 ? WHT : GRY, true, AlignmentType.CENTER),
            ]
          })))
        ]
      }),

      spacer(160),
      h2("11.2 Known Limitations"),
      bullet("The delay loop (DELAY_SHORT) uses a fixed NOP count and is therefore sensitive to host CPU speed. Setting EMU8086 to maximum speed is strongly recommended."),
      bullet("Only one bullet can be in flight at a time. This is a deliberate design decision, not a bug — it prevents trivial balloon-clearing by rapid fire."),
      bullet("The pseudo-random column reset is deterministic (based on the current column value), so after several runs the spawn pattern can become predictable."),
      bullet("No high-score persistence: the program does not write the score to disk between sessions."),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 12. CHALLENGES ══════════════
      h1("12. Challenges & Solutions"),
      spacer(80),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3600, 5760],
        rows: [
          new TableRow({ children: [thCell("Challenge", 3600), thCell("Solution Applied", 5760)] }),
          ...([
            ["Long-distance jump from inside nested loops to GAME OVER handler exceeded JE range", "Introduced the 'ended' flag (DB). Loop sets it and completes normally; GAME_LOOP checks and branches after loop exit."],
            ["Stack corruption when CX (LOOP counter) was clobbered inside the balloon update inner block", "Added PUSH CX / POP CX around every nested block that modifies CX, following Lab 13 discipline."],
            ["Bullet left ghost pixels if not erased before moving", "Every move follows Erase → Update position → Redraw pattern strictly across both bullet and balloon procedures."],
            ["Decimal display of the 16-bit score value", "Implemented PRINT_DEC using repeated DIV by 10 with PUSH/POP digit reversal (Lab 07 + Lab 13)."],
            ["Achieving balloon colour animation without a separate timer", "Used ROL on the 'anim' byte each tick (Lab 11), then isolated bit-0 with AND (Lab 09) to alternate colours."],
            ["Keeping the game non-blocking (no keyboard freeze)", "Used INT 16h AH=01h (poll, not read) so the game loop continues running whether or not a key is pressed."],
          ].map((r, i) => new TableRow({
            children: [
              tdCell(r[0], 3600, i % 2 === 0 ? WHT : GRY),
              tdCell(r[1], 5760, i % 2 === 0 ? WHT : GRY),
            ]
          })))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // ═══════════════ 13. CONCLUSION ═════════════
      h1("13. Conclusion"),
      body("BALLOON POP! successfully demonstrates the full scope of an 8086 assembly-language curriculum through a single, integrated, playable game. Every concept from Labs 01 through 13 is present, purposeful, and documented — from BIOS interrupt usage (Lab 01) and register manipulation (Lab 02) through to stack-disciplined modular procedures (Labs 12 and 13)."),
      spacer(80),
      body("The project reinforces several important principles of low-level programming: the importance of a strict separation between data and code segments, the efficiency gains from using registers intelligently, and the discipline required when managing the stack manually across multiple levels of procedure calls."),
      spacer(80),
      body("Beyond the academic requirements, the game is genuinely playable and visually coherent in the EMU8086 environment, demonstrating that compelling interactive software can be built at the register level without any operating-system abstractions or high-level language support."),

      spacer(160),
      h2("13.1 Future Enhancements"),
      bullet("Difficulty progression — increase BAL_TICKS descent speed as balloons are popped."),
      bullet("Multiple bullet support — allow 2–3 simultaneous bullets in flight."),
      bullet("High-score persistence — write the best score to a text file using INT 21h file services."),
      bullet("Sound effects — use INT 61h / port 42h to generate tones on balloon pop and life loss."),
      bullet("Multi-level gameplay — add a second wave of balloons after the first set is cleared."),

      spacer(200),
      new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 6, color: LBL, space: 4 } },
        spacing: { before: 160, after: 60 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "— End of Report —", font: "Arial", size: 20, color: LBL, italics: true })]
      }),

    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outputPath = path.join(process.cwd(), "BALLOON_POP_Project_Report.docx");
  fs.writeFileSync(outputPath, buffer);
  console.log("Done.");
});