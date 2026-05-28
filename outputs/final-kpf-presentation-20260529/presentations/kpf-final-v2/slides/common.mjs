import path from "node:path";

export const C = {
  ink: "#16202A",
  muted: "#5A6573",
  paper: "#FFFFFF",
  bg: "#F5F2EA",
  line: "#CFD7DE",
  blue: "#2357A6",
  teal: "#158C86",
  green: "#2F7D4E",
  red: "#B94747",
  amber: "#D59332",
  navy: "#0D2B45",
  softBlue: "#E8EEF8",
  softTeal: "#E2F2F0",
  softGreen: "#E8F2EA",
  softRed: "#F7E8E8",
  softAmber: "#F7EEDC",
  dark: "#1F2933",
};

export const COVER_IMAGE = path.resolve(
  process.cwd(),
  "results",
  "final_presentation_assets",
  "kpf-cover-generated.png",
);

export function bg(slide, ctx, color = C.bg) {
  ctx.addShape(slide, { x: 0, y: 0, width: 1280, height: 720, fill: color });
}

export function title(slide, ctx, eyebrow, headline, sub = "") {
  ctx.addText(slide, {
    text: eyebrow,
    x: 56,
    y: 32,
    width: 760,
    height: 24,
    fontSize: 13,
    color: C.teal,
    bold: true,
    typeface: "Malgun Gothic",
  });
  ctx.addText(slide, {
    text: headline,
    x: 56,
    y: 65,
    width: 980,
    height: 62,
    fontSize: 27,
    color: C.ink,
    bold: true,
    typeface: "Malgun Gothic",
  });
  if (sub) {
    ctx.addText(slide, {
      text: sub,
      x: 58,
      y: 136,
      width: 1020,
      height: 38,
      fontSize: 14,
      color: C.muted,
      typeface: "Malgun Gothic",
    });
  }
}

export function footer(slide, ctx, page, total = 12) {
  ctx.addText(slide, {
    text: `K-Privacy Filter 최종 발표 | ${page}/${total}`,
    x: 56,
    y: 684,
    width: 300,
    height: 18,
    fontSize: 9,
    color: "#7A8491",
    typeface: "Malgun Gothic",
  });
  ctx.addText(slide, {
    text: "Evidence: repository, Colab runs, Drive artifacts, 2026-05-29",
    x: 770,
    y: 684,
    width: 454,
    height: 18,
    fontSize: 9,
    color: "#7A8491",
    align: "right",
    typeface: "Aptos",
  });
}

export function card(slide, ctx, x, y, w, h, fill = C.paper, line = C.line) {
  ctx.addShape(slide, {
    x,
    y,
    width: w,
    height: h,
    fill,
    line: { fill: line, width: 1, style: "solid" },
  });
}

export function label(slide, ctx, text, x, y, w, fill = C.softTeal, color = C.ink) {
  ctx.addShape(slide, { x, y, width: w, height: 28, fill, line: { fill, width: 1, style: "solid" } });
  ctx.addText(slide, {
    text,
    x: x + 10,
    y: y + 6,
    width: w - 20,
    height: 16,
    fontSize: 10,
    color,
    bold: true,
    align: "center",
    typeface: "Malgun Gothic",
  });
}

export function metric(slide, ctx, x, y, w, labelText, value, note, color = C.blue) {
  ctx.addText(slide, {
    text: value,
    x,
    y,
    width: w,
    height: 42,
    fontSize: 29,
    color,
    bold: true,
    align: "center",
    typeface: "Aptos Display",
  });
  ctx.addText(slide, {
    text: labelText,
    x,
    y: y + 45,
    width: w,
    height: 20,
    fontSize: 11,
    color: C.ink,
    bold: true,
    align: "center",
    typeface: "Malgun Gothic",
  });
  ctx.addText(slide, {
    text: note,
    x,
    y: y + 67,
    width: w,
    height: 36,
    fontSize: 9,
    color: C.muted,
    align: "center",
    typeface: "Malgun Gothic",
  });
}

export function bullet(slide, ctx, text, x, y, w, color = C.ink) {
  ctx.addShape(slide, { x, y: y + 7, width: 6, height: 6, fill: C.teal });
  ctx.addText(slide, {
    text,
    x: x + 15,
    y,
    width: w - 15,
    height: 32,
    fontSize: 13,
    color,
    typeface: "Malgun Gothic",
  });
}

export function smallText(slide, ctx, text, x, y, w, h, size = 11, color = C.muted) {
  ctx.addText(slide, {
    text,
    x,
    y,
    width: w,
    height: h,
    fontSize: size,
    color,
    typeface: "Malgun Gothic",
  });
}

export function table(slide, ctx, x, y, widths, rows, opts = {}) {
  const rowH = opts.rowH || 42;
  const headFill = opts.headFill || C.navy;
  const bodyFill = opts.bodyFill || C.paper;
  let yy = y;
  rows.forEach((row, ri) => {
    let xx = x;
    const fill = ri === 0 ? headFill : bodyFill;
    const color = ri === 0 ? "#FFFFFF" : C.ink;
    widths.forEach((w, ci) => {
      ctx.addShape(slide, { x: xx, y: yy, width: w, height: rowH, fill, line: { fill: C.line, width: 1, style: "solid" } });
      ctx.addText(slide, {
        text: row[ci],
        x: xx + 8,
        y: yy + 9,
        width: w - 16,
        height: rowH - 12,
        fontSize: ri === 0 ? 10 : 11,
        color,
        bold: ri === 0,
        align: ci === 0 ? "left" : "center",
        typeface: ci === 0 ? "Malgun Gothic" : "Aptos",
      });
      xx += w;
    });
    yy += rowH;
  });
}

export function flowBox(slide, ctx, x, y, w, titleText, body, fill = C.paper) {
  card(slide, ctx, x, y, w, 92, fill);
  ctx.addText(slide, { text: titleText, x: x + 14, y: y + 13, width: w - 28, height: 22, fontSize: 13, bold: true, color: C.ink, typeface: "Malgun Gothic" });
  ctx.addText(slide, { text: body, x: x + 14, y: y + 40, width: w - 28, height: 42, fontSize: 10.5, color: C.muted, typeface: "Malgun Gothic" });
}

export function arrow(slide, ctx, x1, y1, x2, y2, color = C.teal) {
  ctx.addShape(slide, {
    shape: "line",
    x: x1,
    y: y1,
    width: x2 - x1,
    height: y2 - y1,
    line: { fill: color, width: 2.2, beginArrowType: "none", endArrowType: "triangle", style: "solid" },
  });
}
