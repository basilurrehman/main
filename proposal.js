const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
  UnderlineType
} = require('docx');
const fs = require('fs');
const path = require('path');

// ── Colours ───────────────────────────────────────────────────
const NAVY   = "1F3864";
const BLUE   = "2E5FA3";
const LBLUE  = "D6E4F7";
const MID    = "4472C4";
const WHITE  = "FFFFFF";
const LGREY  = "F2F2F2";
const MGREY  = "D9D9D9";
const BLACK  = "000000";

// ── Borders ───────────────────────────────────────────────────
const thinBorder  = { style: BorderStyle.SINGLE, size: 4,  color: "AAAAAA" };
const thickBorder = { style: BorderStyle.SINGLE, size: 12, color: NAVY };
const cellBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorder    = { style: BorderStyle.NIL, size: 0, color: "FFFFFF" };
const noBorders   = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

const PAGE_W   = 12240;  // US Letter
const PAGE_H   = 15840;
const MARGIN   = 1080;   // 0.75"
const CONTENT  = PAGE_W - MARGIN * 2; // 10080 DXA

// ── Helper: standard body text ────────────────────────────────
const body = (text, opts = {}) => new Paragraph({
  alignment: opts.center ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
  spacing: { before: 60, after: 60, line: 276 },
  children: [new TextRun({
    text,
    font: "Times New Roman",
    size: 22,
    bold: opts.bold || false,
    italics: opts.italic || false,
    color: opts.color || BLACK,
  })]
});

// ── Helper: section label row (dark header) ───────────────────
const sectionRow = (label) => new TableRow({
  children: [new TableCell({
    columnSpan: 2,
    borders: cellBorders,
    shading: { fill: NAVY, type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 150, right: 150 },
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      children: [new TextRun({
        text: label,
        font: "Arial",
        size: 22,
        bold: true,
        color: WHITE,
      })]
    })]
  })]
});

// ── Helper: content row ───────────────────────────────────────
const contentRow = (paragraphs) => new TableRow({
  children: [new TableCell({
    columnSpan: 2,
    borders: cellBorders,
    shading: { fill: WHITE, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 150, right: 150 },
    children: paragraphs
  })]
});

// ── Helper: two-column info row ───────────────────────────────
const infoRow = (leftLabel, leftVal, rightLabel, rightVal) => new TableRow({
  children: [
    new TableCell({
      width: { size: CONTENT / 2, type: WidthType.DXA },
      borders: cellBorders,
      shading: { fill: LGREY, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 150, right: 150 },
      children: [new Paragraph({
        children: [
          new TextRun({ text: leftLabel + " ", font: "Arial", size: 20, bold: true }),
          new TextRun({ text: leftVal,          font: "Arial", size: 20 }),
        ]
      })]
    }),
    new TableCell({
      width: { size: CONTENT / 2, type: WidthType.DXA },
      borders: cellBorders,
      shading: { fill: LGREY, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 150, right: 150 },
      children: [new Paragraph({
        children: [
          new TextRun({ text: rightLabel + " ", font: "Arial", size: 20, bold: true }),
          new TextRun({ text: rightVal,          font: "Arial", size: 20 }),
        ]
      })]
    }),
  ]
});

// ── Helper: bullet paragraph ──────────────────────────────────
const bullet = (text, sub = false) => new Paragraph({
  numbering: { reference: "bullets", level: sub ? 1 : 0 },
  spacing: { before: 40, after: 40, line: 260 },
  children: [new TextRun({ text, font: "Times New Roman", size: 21 })]
});

const numberedItem = (text, ref = "numbers") => new Paragraph({
  numbering: { reference: ref, level: 0 },
  spacing: { before: 50, after: 50, line: 260 },
  children: [new TextRun({ text, font: "Times New Roman", size: 21 })]
});

const cellPara = (text, opts = {}) => new Paragraph({
  alignment: opts.center ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
  spacing: { before: 60, after: 60, line: 276 },
  children: [new TextRun({
    text,
    font: "Times New Roman",
    size: 21,
    bold:    opts.bold    || false,
    italics: opts.italic  || false,
    color:   opts.color   || BLACK,
  })]
});

// ── Blank spacer paragraph ────────────────────────────────────
const spacer = (pts = 60) => new Paragraph({
  spacing: { before: pts, after: pts },
  children: [new TextRun({ text: "" })]
});

// =============================================================
//  D O C U M E N T
// =============================================================
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0, format: LevelFormat.BULLET, text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 540, hanging: 270 } } }
          },
          {
            level: 1, format: LevelFormat.BULLET, text: "\u25CB",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 900, hanging: 270 } } }
          }
        ]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 270 } } }
        }]
      },
      {
        reference: "alpha",
        levels: [{
          level: 0, format: LevelFormat.LOWER_LETTER, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 270 } } }
        }]
      },
    ]
  },

  styles: {
    default: {
      document: { run: { font: "Times New Roman", size: 22 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: NAVY },
        paragraph: { spacing: { before: 300, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: BLUE },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 }
      },
    ]
  },

  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
      }
    },

    // ── HEADER ──────────────────────────────────────────────
    headers: {
      default: new Header({
        children: [
          // University name bar
          new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 4 } },
            spacing: { before: 0, after: 80 },
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "BAHRIA UNIVERSITY, KARACHI CAMPUS", font: "Arial", size: 22, bold: true, color: NAVY }),
              new TextRun({ text: "   |   Department of Computer Science", font: "Arial", size: 20, color: BLUE }),
            ]
          }),
        ]
      })
    },

    children: [

      // ═══════════════════════════════════════════════════════
      //  COVER TITLE BLOCK
      // ═══════════════════════════════════════════════════════
      spacer(160),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "PROJECT PROPOSAL", font: "Arial", size: 52, bold: true, color: NAVY })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 4 } },
        children: [new TextRun({ text: "Computer Organization and Assembly Language  \u2014  CEL-323", font: "Arial", size: 24, italics: true, color: BLUE })]
      }),

      spacer(120),

      // ═══════════════════════════════════════════════════════
      //  COURSE INFO TABLE
      // ═══════════════════════════════════════════════════════
      new Table({
        width: { size: CONTENT, type: WidthType.DXA },
        columnWidths: [CONTENT / 2, CONTENT / 2],
        rows: [
          infoRow("Course Title:",       "Computer Organization and Assembly Language",
                  "Course Code:",        "CEL-323"),
          infoRow("Course Instructor:",  "Sir Rao Awais",
                  "Class:",              "BS (CS) \u2013 4A  |  Spring 2026"),
          infoRow("Senior Lab Instructor:", "Ma\u2019am Mehwish Saleem",
                  "Submission Date:",    "____________"),
          infoRow("Student Name:",       "Basil Ur Rehman",
                  "Enrollment No.:",     "02-134242-113"),
        ]
      }),

      spacer(200),

      // ═══════════════════════════════════════════════════════
      //  MAIN PROPOSAL TABLE
      // ═══════════════════════════════════════════════════════
      new Table({
        width: { size: CONTENT, type: WidthType.DXA },
        columnWidths: [CONTENT / 2, CONTENT / 2],
        rows: [

          // ── PROJECT TITLE ─────────────────────────────────
          sectionRow("1.   PROJECT TITLE"),
          contentRow([
            new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { before: 80, after: 80 },
              children: [new TextRun({
                text: "BALLOON POP!  \u2014  A Real-Time Interactive ASCII Game in 8086 Assembly Language",
                font: "Arial", size: 24, bold: true, color: NAVY
              })]
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { before: 0, after: 80 },
              children: [new TextRun({
                text: "Developed for EMU8086  |  CEL-323 Final Lab Project  |  Spring 2026",
                font: "Times New Roman", size: 20, italics: true, color: BLUE
              })]
            }),
          ]),

          // ── GROUP MEMBERS ─────────────────────────────────
          sectionRow("2.   GROUP MEMBERS  \u2039Solo Project\u203A"),
          new TableRow({
            children: [
              new TableCell({
                columnSpan: 2,
                borders: cellBorders,
                shading: { fill: WHITE, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 150, right: 150 },
                children: [
                  new Table({
                    width: { size: CONTENT - 300, type: WidthType.DXA },
                    columnWidths: [800, 3300, 2900, 2780],
                    rows: [
                      // Header
                      new TableRow({
                        children: [
                          new TableCell({
                            width: { size: 800, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: BLUE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "S. No.", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                          }),
                          new TableCell({
                            width: { size: 3300, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: BLUE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Student Name", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                          }),
                          new TableCell({
                            width: { size: 2900, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: BLUE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Enrollment No.", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                          }),
                          new TableCell({
                            width: { size: 2780, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: BLUE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Role", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                          }),
                        ]
                      }),
                      // Student row
                      new TableRow({
                        children: [
                          new TableCell({
                            width: { size: 800, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: LGREY, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "01", font: "Times New Roman", size: 21 })] })]
                          }),
                          new TableCell({
                            width: { size: 3300, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: LGREY, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ children: [new TextRun({ text: "Basil Ur Rehman", font: "Times New Roman", size: 21 })] })]
                          }),
                          new TableCell({
                            width: { size: 2900, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: LGREY, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "02-134242-113", font: "Times New Roman", size: 21 })] })]
                          }),
                          new TableCell({
                            width: { size: 2780, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: LGREY, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Lead Developer", font: "Times New Roman", size: 21, bold: true })] })]
                          }),
                        ]
                      }),
                    ]
                  })
                ]
              })
            ]
          }),

          // ── PROJECT SCOPE ─────────────────────────────────
          sectionRow("3.   PROJECT SCOPE"),
          contentRow([
            cellPara(
              "This project involves the design and implementation of a real-time, interactive, " +
              "multi-entity ASCII game using 8086 Assembly Language executed within the EMU8086 " +
              "emulation environment. The scope of the project encompasses direct hardware-level " +
              "programming through BIOS (INT 10h) and DOS (INT 21h) interrupt service routines for " +
              "screen rendering and output, without any high-level language abstraction or runtime library support."
            ),
            spacer(40),
            cellPara(
              "The system employs a polling-based, non-blocking keyboard input mechanism via BIOS " +
              "INT 16h, a frame-tick-driven game loop with independent speed counters for each entity " +
              "class, and parallel byte-array data structures for simultaneous multi-entity management. " +
              "The project is scoped to integrate and demonstrate the complete CEL-323 laboratory " +
              "curriculum \u2014 Labs 01 through 13 \u2014 within a single, cohesive, self-contained " +
              "application binary."
            ),
          ]),

          // ── PROJECT ABSTRACT ──────────────────────────────
          sectionRow("4.   PROJECT ABSTRACT"),
          contentRow([
            cellPara(
              "BALLOON POP! is a real-time ASCII-graphics game implemented entirely in 8086 assembly " +
              "language for the EMU8086 emulation platform. The program renders five dynamically animated " +
              "balloon entities on an 80\u00D725 character-mode display using BIOS INT 10h video services, " +
              "employing a cannon-based projectile mechanism controlled through keyboard input. Entity " +
              "states, positions, and lifecycle flags are maintained in parallel byte arrays indexed " +
              "via the SI register, constituting a lightweight, memory-efficient entity-component model " +
              "at the assembly level."
            ),
            spacer(40),
            cellPara(
              "The program architecture is fully modular, comprising twelve isolated procedures " +
              "covering screen I/O, collision detection, HUD management, and sprite animation. A " +
              "software-defined game loop synchronises entity movement across independent timelines " +
              "using frame-tick counters and NOP-based delay subroutines. Projectile-balloon collision " +
              "detection is implemented through indexed array traversal with a proximity-tolerance " +
              "algorithm operating on both row and column axes. The project integrates all thirteen " +
              "COAL laboratory concepts \u2014 from basic interrupt-driven I/O (Lab 01) through bitwise " +
              "shift and rotate operations (Labs 10\u201311) and stack-based register preservation (Lab 13) " +
              "\u2014 into a single executable application, demonstrating mastery of low-level systems " +
              "programming at the instruction-set architecture level."
            ),
          ]),

          // ── PROJECT FUNCTIONALITIES ───────────────────────
          sectionRow("5.   PROJECT FUNCTIONALITIES"),
          new TableRow({
            children: [new TableCell({
              columnSpan: 2,
              borders: cellBorders,
              shading: { fill: WHITE, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 150, right: 150 },
              children: [
                // Core features
                new Paragraph({
                  spacing: { before: 0, after: 60 },
                  children: [new TextRun({ text: "A.  Core Game Mechanics", font: "Arial", size: 22, bold: true, color: BLUE })]
                }),
                numberedItem("Real-time non-blocking keyboard polling (INT 16h AH=01h) for cannon movement via [A]/[D] keys and single-shot projectile firing via [SPACE]; duplicate-fire prevention enforced through a binary fly-flag."),
                numberedItem("Frame-tick-driven entity update loop with two independent 16-bit DW counters controlling balloon descent speed and bullet ascent speed, each configurable via EQU constants for emulation-speed portability."),
                numberedItem("Five simultaneous balloon entities managed through three parallel DB arrays (column, row, live-flag), traversed by SI-register indexed addressing within a CX-driven LOOP construct."),
                numberedItem("Projectile-balloon collision detection via a two-axis proximity algorithm: exact row match followed by absolute column difference check (\u22643 character tolerance), using SUB and NEG (two\u2019s complement sign correction) for branchless absolute-value computation."),
                numberedItem("Pseudo-random balloon X-position recalculation on escape using SHL (Lab 10) and AND bitmask (Lab 09) on the prior column value, preventing deterministic re-entry paths."),
                spacer(60),

                // Display features
                new Paragraph({
                  spacing: { before: 0, after: 60 },
                  children: [new TextRun({ text: "B.  Display and Rendering", font: "Arial", size: 22, bold: true, color: BLUE })]
                }),
                numberedItem("BIOS-level coloured character rendering through INT 10h AH=09h with explicit attribute byte (foreground | background) control, producing bright-green cannon, yellow bullet, and alternating red/cyan balloon sprites."),
                numberedItem("ROL-driven two-frame balloon colour animation: a single DB animation byte is rotated left (Lab 11) each game tick, and bit-0 is isolated via AND (Lab 09) to select between two colour attributes, producing a twinkling visual effect without additional variables."),
                numberedItem("Real-time HUD refresh on row 0 displaying score (16-bit DW) and lives (8-bit DB), with decimal conversion implemented via iterative DIV-10 digit extraction and LIFO stack re-ordering (Lab 13) for correct most-significant-digit-first output."),
                numberedItem("Static border and control-instruction rendering at game initialisation using INT 21h AH=09h dollar-terminated string output (Lab 03), with cursor concealment via INT 10h AH=01h for a clean game display."),
                spacer(60),

                // End-state features
                new Paragraph({
                  spacing: { before: 0, after: 60 },
                  children: [new TextRun({ text: "C.  Game States and Flow Control", font: "Arial", size: 22, bold: true, color: BLUE })]
                }),
                numberedItem("Three-lives system with per-balloon-escape decrement; a deferred end-state flag (DB ended) prevents mid-LOOP stack imbalance by deferring the game-over branch until after all PUSH/POP pairs in the balloon update loop are resolved."),
                numberedItem("Win detection on n_pop = NUM_BAL (all five balloons popped), triggering a dedicated SHOW_WIN screen; loss detection on lives = 0, triggering SHOW_GAME_OVER, both displaying the final score via PRINT_DEC before a blocking INT 16h AH=00h keypress wait."),
                numberedItem("Graceful exit with cursor restoration (INT 10h AH=01h CX=0607h) and DOS process termination via INT 21h AH=4Ch (Lab 01), ensuring clean EMU8086 environment state on game end or user-initiated quit [Q]."),
              ]
            })]
          }),

          // ── MODULE DISTRIBUTION ───────────────────────────
          sectionRow("6.   MODULE DISTRIBUTION"),
          new TableRow({
            children: [new TableCell({
              columnSpan: 2,
              borders: cellBorders,
              shading: { fill: WHITE, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 100, left: 150, right: 150 },
              children: [
                new Paragraph({
                  spacing: { before: 0, after: 80 },
                  children: [
                    new TextRun({ text: "Sole Developer: ", font: "Arial", size: 21, bold: true }),
                    new TextRun({ text: "Basil Ur Rehman (02-134242-113) \u2014 all modules designed, coded, and tested independently.", font: "Times New Roman", size: 21 }),
                  ]
                }),
                // Module distribution table
                new Table({
                  width: { size: CONTENT - 300, type: WidthType.DXA },
                  columnWidths: [1400, 3200, 5180],
                  rows: [
                    // Header row
                    new TableRow({
                      children: [
                        new TableCell({
                          width: { size: 1400, type: WidthType.DXA },
                          borders: cellBorders,
                          shading: { fill: BLUE, type: ShadingType.CLEAR },
                          margins: { top: 60, bottom: 60, left: 100, right: 100 },
                          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Module", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                        }),
                        new TableCell({
                          width: { size: 3200, type: WidthType.DXA },
                          borders: cellBorders,
                          shading: { fill: BLUE, type: ShadingType.CLEAR },
                          margins: { top: 60, bottom: 60, left: 100, right: 100 },
                          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Procedures / Components", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                        }),
                        new TableCell({
                          width: { size: 5180, type: WidthType.DXA },
                          borders: cellBorders,
                          shading: { fill: BLUE, type: ShadingType.CLEAR },
                          margins: { top: 60, bottom: 60, left: 100, right: 100 },
                          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "COAL Labs Demonstrated", font: "Arial", size: 20, bold: true, color: WHITE })] })]
                        }),
                      ]
                    }),
                    // Row data helper
                    ...([
                      ["Module 1", "MAIN, Game Loop, Keyboard Dispatch (DO_LEFT, DO_RIGHT, DO_FIRE)",
                       "Lab 01 (INT 16h), Lab 02 (AX/AL), Lab 04 (Immediate/Direct), Lab 05 (CMP/JE/JBE/JAE)"],
                      ["Module 2", "DRAW_CANNON, ERASE_CANNON, PUTCHAT, GOTOXY, CLR_SCR",
                       "Lab 01 (INT 10h), Lab 07 (INC/ADD), Lab 09 (colour attributes), Lab 13 (PUSH/POP)"],
                      ["Module 3", "DRAW_BAL, ERASE_BAL, DRAW_BULLET, ERASE_BULLET",
                       "Lab 04 (Indexed addr.), Lab 07 (INC), Lab 09 (AND), Lab 11 (ROL), Lab 13 (PUSH/POP)"],
                      ["Module 4", "CHECK_HIT (collision detection)",
                       "Lab 05 (JE/JNE/JG), Lab 06 (LOOP), Lab 07 (SUB), Lab 08 (Arrays), Lab 09 (TEST/NEG)"],
                      ["Module 5", "Balloon tick update, life deduction, pseudo-random X reset",
                       "Lab 06 (LOOP), Lab 08 (Arrays), Lab 09 (AND), Lab 10 (SHL), Lab 13 (PUSH/POP)"],
                      ["Module 6", "DRAW_HUD, PRINT_DEC, DRAW_FRAME",
                       "Lab 01 (INT 21h), Lab 03 (DB/DW/Strings), Lab 07 (DIV/ADD), Lab 13 (PUSH/POP stack)"],
                      ["Module 7", "DELAY_SHORT, end-state screens (SHOW_WIN, SHOW_GAME_OVER, DO_QUIT)",
                       "Lab 01 (INT 21h/16h/10h), Lab 04 (Immediate), Lab 06 (LOOP / NOP delay)"],
                    ]).map(([mod, procs, labs], i) =>
                      new TableRow({
                        children: [
                          new TableCell({
                            width: { size: 1400, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: i % 2 === 0 ? LGREY : WHITE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            verticalAlign: VerticalAlign.TOP,
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: mod, font: "Arial", size: 20, bold: true })] })]
                          }),
                          new TableCell({
                            width: { size: 3200, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: i % 2 === 0 ? LGREY : WHITE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            verticalAlign: VerticalAlign.TOP,
                            children: [new Paragraph({ children: [new TextRun({ text: procs, font: "Times New Roman", size: 20 })] })]
                          }),
                          new TableCell({
                            width: { size: 5180, type: WidthType.DXA },
                            borders: cellBorders,
                            shading: { fill: i % 2 === 0 ? LGREY : WHITE, type: ShadingType.CLEAR },
                            margins: { top: 60, bottom: 60, left: 100, right: 100 },
                            verticalAlign: VerticalAlign.TOP,
                            children: [new Paragraph({ children: [new TextRun({ text: labs, font: "Times New Roman", size: 20, italics: true })] })]
                          }),
                        ]
                      })
                    )
                  ]
                }),
              ]
            })]
          }),

        ] // end main table rows
      }), // end main Table

      spacer(200),

      // ═══════════════════════════════════════════════════════
      //  SIGNATURE BLOCK
      // ═══════════════════════════════════════════════════════
      new Table({
        width: { size: CONTENT, type: WidthType.DXA },
        columnWidths: [CONTENT / 2, CONTENT / 2],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                width: { size: CONTENT / 2, type: WidthType.DXA },
                borders: cellBorders,
                shading: { fill: LGREY, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 150, right: 150 },
                children: [
                  new Paragraph({ children: [new TextRun({ text: "Teacher Signature:", font: "Arial", size: 21, bold: true })] }),
                  spacer(100),
                  new Paragraph({
                    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "999999" } },
                    children: [new TextRun({ text: " ", font: "Arial", size: 21 })]
                  }),
                ]
              }),
              new TableCell({
                width: { size: CONTENT / 2, type: WidthType.DXA },
                borders: cellBorders,
                shading: { fill: LGREY, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 150, right: 150 },
                children: [
                  new Paragraph({ children: [new TextRun({ text: "Remarks:", font: "Arial", size: 21, bold: true })] }),
                  spacer(100),
                  new Paragraph({
                    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "999999" } },
                    children: [new TextRun({ text: " ", font: "Arial", size: 21 })]
                  }),
                ]
              }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                columnSpan: 2,
                borders: cellBorders,
                shading: { fill: LGREY, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 150, right: 150 },
                children: [
                  new Paragraph({ children: [
                    new TextRun({ text: "Submission Date:  ", font: "Arial", size: 21, bold: true }),
                    new TextRun({ text: "___________________", font: "Arial", size: 21 }),
                    new TextRun({ text: "          Grade / Marks:  ", font: "Arial", size: 21, bold: true }),
                    new TextRun({ text: "___________________", font: "Arial", size: 21 }),
                  ]})
                ]
              })
            ]
          })
        ]
      }),

      spacer(60),

    ] // end children
  }]
});

// Write file
Packer.toBuffer(doc).then(buf => {
  const outputPath = path.join(process.cwd(), "COAL_Project_Proposal_BasilUrRehman.docx");
  fs.writeFileSync(outputPath, buf);
  console.log("Done", outputPath);
});