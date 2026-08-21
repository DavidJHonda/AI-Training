#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let outputPaths = [
    "board-review-first-four/alternatives/understand-ai/how-ai-answers-last-token-alternative.jpg",
    "illustrations/how-ai-answers-last-token.jpg",
    "lessons/how-ai-answers-last-token.jpg"
]

let width: CGFloat = 1600
let height: CGFloat = 900

func color(_ hex: String, alpha: CGFloat = 1) -> NSColor {
    let clean = hex.replacingOccurrences(of: "#", with: "")
    var value: UInt64 = 0
    Scanner(string: clean).scanHexInt64(&value)
    return NSColor(
        calibratedRed: CGFloat((value >> 16) & 0xff) / 255,
        green: CGFloat((value >> 8) & 0xff) / 255,
        blue: CGFloat(value & 0xff) / 255,
        alpha: alpha
    )
}

let lavender = color("#eeeaff")
let navy = color("#08072b")
let muted = color("#655f7c")
let purple = color("#6f52ff")
let teal = color("#14968f")
let gold = color("#ffe9ab")
let rule = color("#e3def2")
let palePurple = color("#f4f0ff")
let paleTeal = color("#e7f7f4")
let rowFill = color("#faf9ff")

func loadFont(path: String, size: CGFloat) -> NSFont {
    let url = URL(fileURLWithPath: path)
    CTFontManagerRegisterFontsForURL(url as CFURL, .process, nil)
    if let descriptors = CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],
       let descriptor = descriptors.first,
       let postscriptName = CTFontDescriptorCopyAttribute(descriptor, kCTFontNameAttribute) as? String,
       let font = NSFont(name: postscriptName, size: size) {
        return font
    }
    return NSFont.systemFont(ofSize: size)
}

let fontRoot = "/Users/davidobrien/Library/Fonts"
func heavy(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Heavy.otf", size: size) }
func demi(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Demi.otf", size: size) }
func medium(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Medium.otf", size: size) }

func roundedRect(_ rect: NSRect, radius: CGFloat, fill: NSColor, stroke: NSColor? = nil, lineWidth: CGFloat = 1) {
    let path = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
    fill.setFill()
    path.fill()
    if let stroke {
        stroke.setStroke()
        path.lineWidth = lineWidth
        path.stroke()
    }
}

func drawText(
    _ value: String,
    in rect: NSRect,
    font: NSFont,
    color: NSColor,
    alignment: NSTextAlignment = .left,
    lineHeight: CGFloat? = nil
) {
    let paragraph = NSMutableParagraphStyle()
    paragraph.alignment = alignment
    if let lineHeight {
        paragraph.minimumLineHeight = lineHeight
        paragraph.maximumLineHeight = lineHeight
    }
    (value as NSString).draw(in: rect, withAttributes: [
        .font: font,
        .foregroundColor: color,
        .paragraphStyle: paragraph
    ])
}

func textSize(_ value: String, font: NSFont) -> NSSize {
    (value as NSString).size(withAttributes: [.font: font])
}

func centeredText(_ value: String, center: NSPoint, font: NSFont, color: NSColor) {
    let size = textSize(value, font: font)
    drawText(
        value,
        in: NSRect(x: center.x - size.width / 2, y: center.y - size.height / 2 - 1, width: size.width + 4, height: size.height + 6),
        font: font,
        color: color,
        alignment: .center
    )
}

func line(from start: NSPoint, to end: NSPoint, color: NSColor, width: CGFloat = 2) {
    let path = NSBezierPath()
    path.move(to: start)
    path.line(to: end)
    path.lineWidth = width
    path.lineCapStyle = .round
    color.setStroke()
    path.stroke()
}

func drawArrow(from start: NSPoint, to end: NSPoint, color: NSColor, width: CGFloat = 4) {
    line(from: start, to: end, color: color, width: width)
    let angle = atan2(end.y - start.y, end.x - start.x)
    for offset in [CGFloat.pi * 0.82, -CGFloat.pi * 0.82] {
        let point = NSPoint(x: end.x + 13 * cos(angle + offset), y: end.y + 13 * sin(angle + offset))
        line(from: end, to: point, color: color, width: width)
    }
}

func drawCheckBand(_ takeaway: String) {
    roundedRect(NSRect(x: 80, y: 776, width: 1440, height: 84), radius: 16, fill: gold)
    let font = demi(31)
    let size = textSize(takeaway, font: font)
    let lockupWidth: CGFloat = 52 + 16 + size.width
    let x = (width - lockupWidth) / 2
    roundedRect(NSRect(x: x, y: 792, width: 52, height: 52), radius: 26, fill: purple)

    let check = NSBezierPath()
    check.move(to: NSPoint(x: x + 14, y: 818))
    check.line(to: NSPoint(x: x + 23, y: 827))
    check.line(to: NSPoint(x: x + 39, y: 807))
    check.lineWidth = 5
    check.lineCapStyle = .round
    check.lineJoinStyle = .round
    NSColor.white.setStroke()
    check.stroke()
    drawText(takeaway, in: NSRect(x: x + 68, y: 800, width: size.width + 4, height: 46), font: font, color: navy)
}

func drawWordPill(_ value: String, center: NSPoint, emphasized: Bool = false) {
    let font = emphasized ? demi(25) : medium(24)
    let size = textSize(value, font: font)
    let pillWidth = max(58, size.width + 30)
    roundedRect(
        NSRect(x: center.x - pillWidth / 2, y: center.y - 25, width: pillWidth, height: 50),
        radius: 12,
        fill: emphasized ? purple : NSColor.white,
        stroke: emphasized ? purple : rule,
        lineWidth: emphasized ? 2 : 1.5
    )
    centeredText(value, center: center, font: font, color: emphasized ? .white : navy)
}

func drawScoreRow(y: CGFloat, token: String, score: Int, emphasized: Bool = false) {
    roundedRect(
        NSRect(x: 1100, y: y, width: 336, height: 72),
        radius: 12,
        fill: emphasized ? palePurple : rowFill,
        stroke: emphasized ? purple.withAlphaComponent(0.45) : rule,
        lineWidth: emphasized ? 2 : 1.5
    )
    drawText(token, in: NSRect(x: 1122, y: y + 17, width: 114, height: 38), font: emphasized ? demi(27) : medium(26), color: emphasized ? purple : navy)
    let barWidth = CGFloat(score) / 18 * 132
    roundedRect(NSRect(x: 1240, y: y + 27, width: 132, height: 18), radius: 9, fill: rule)
    roundedRect(NSRect(x: 1240, y: y + 27, width: barWidth, height: 18), radius: 9, fill: emphasized ? purple : color("#b9addd"))
    drawText("\(score)%", in: NSRect(x: 1364, y: y + 17, width: 56, height: 38), font: demi(24), color: emphasized ? purple : muted, alignment: .right)
}

let image = NSImage(size: NSSize(width: width, height: height))
image.lockFocusFlipped(true)
lavender.setFill()
NSRect(x: 0, y: 0, width: width, height: height).fill()

drawText(
    "The last token carries the whole question",
    in: NSRect(x: 80, y: 57, width: 1440, height: 58),
    font: heavy(44),
    color: navy,
    alignment: .center
)
roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)

let questionCard = NSRect(x: 112, y: 210, width: 506, height: 486)
let vectorCard = NSRect(x: 664, y: 210, width: 350, height: 486)
let answerCard = NSRect(x: 1060, y: 210, width: 428, height: 486)
roundedRect(questionCard, radius: 16, fill: rowFill, stroke: rule, lineWidth: 1.5)
roundedRect(vectorCard, radius: 16, fill: palePurple, stroke: purple.withAlphaComponent(0.28), lineWidth: 1.5)
roundedRect(answerCard, radius: 16, fill: paleTeal, stroke: teal.withAlphaComponent(0.35), lineWidth: 1.5)

drawText("THE QUESTION", in: NSRect(x: 136, y: 236, width: 458, height: 34), font: demi(22), color: purple, alignment: .center)
drawText("What should I name", in: NSRect(x: 136, y: 292, width: 458, height: 43), font: demi(31), color: navy, alignment: .center)
drawText("my new dog?", in: NSRect(x: 136, y: 336, width: 458, height: 43), font: demi(31), color: navy, alignment: .center)

let tokenCenters: [(String, NSPoint)] = [
    ("What", NSPoint(x: 177, y: 436)),
    ("should", NSPoint(x: 288, y: 436)),
    ("I", NSPoint(x: 381, y: 436)),
    ("name", NSPoint(x: 476, y: 436)),
    ("my", NSPoint(x: 198, y: 512)),
    ("new", NSPoint(x: 296, y: 512)),
    ("dog", NSPoint(x: 398, y: 512)),
    ("?", NSPoint(x: 525, y: 512))
]
for (token, center) in tokenCenters {
    drawWordPill(token, center: center, emphasized: token == "?")
}

let carryY: CGFloat = 585
line(from: NSPoint(x: 170, y: carryY), to: NSPoint(x: 508, y: carryY), color: purple.withAlphaComponent(0.7), width: 4)
drawArrow(from: NSPoint(x: 508, y: carryY), to: NSPoint(x: 525, y: 543), color: purple, width: 4)
drawText(
    "Attention folds the earlier tokens into the final one.",
    in: NSRect(x: 142, y: 612, width: 446, height: 58),
    font: medium(24),
    color: muted,
    alignment: .center,
    lineHeight: 29
)

drawText("THE LAST TOKEN", in: NSRect(x: 688, y: 236, width: 302, height: 34), font: demi(22), color: purple, alignment: .center)
roundedRect(NSRect(x: 777, y: 294, width: 124, height: 124), radius: 62, fill: purple)
centeredText("?", center: NSPoint(x: 839, y: 356), font: heavy(58), color: .white)
drawText("FINAL VECTOR", in: NSRect(x: 690, y: 455, width: 298, height: 32), font: demi(21), color: muted, alignment: .center)
roundedRect(NSRect(x: 704, y: 498, width: 270, height: 70), radius: 12, fill: .white, stroke: rule, lineWidth: 1.5)
drawText("[−0.96, 1.49, −2.58, …]", in: NSRect(x: 720, y: 518, width: 238, height: 32), font: demi(21), color: purple, alignment: .center)
drawText("Carries the entire\nquestion", in: NSRect(x: 694, y: 588, width: 290, height: 70), font: demi(25), color: navy, alignment: .center, lineHeight: 30)

drawArrow(from: NSPoint(x: 1026, y: 454), to: NSPoint(x: 1048, y: 454), color: purple, width: 4)

drawText("THE NEXT TOKEN", in: NSRect(x: 1084, y: 236, width: 380, height: 34), font: demi(22), color: teal, alignment: .center)
drawText("Reply starters", in: NSRect(x: 1084, y: 286, width: 380, height: 44), font: demi(31), color: navy, alignment: .center)
drawScoreRow(y: 354, token: "YOU", score: 18, emphasized: true)
drawScoreRow(y: 440, token: "A", score: 14)
drawScoreRow(y: 526, token: "GREAT", score: 9)
drawText("First word of the answer", in: NSRect(x: 1084, y: 628, width: 380, height: 38), font: demi(25), color: teal, alignment: .center)

drawCheckBand("The next word goes after the last token, so that’s the vector the model reads.")

image.unlockFocus()
guard let tiff = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let jpeg = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.94]) else {
    fputs("Could not encode How AI Answers board.\n", stderr)
    exit(1)
}

for relativePath in outputPaths {
    let outputURL = repoRoot.appendingPathComponent(relativePath)
    try FileManager.default.createDirectory(at: outputURL.deletingLastPathComponent(), withIntermediateDirectories: true)
    try jpeg.write(to: outputURL)
    print("Built \(outputURL.path)")
}
