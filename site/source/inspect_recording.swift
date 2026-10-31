import Foundation
import AVFoundation
import AppKit

let url = URL(fileURLWithPath: CommandLine.arguments[1])
let output = URL(fileURLWithPath: CommandLine.arguments[2])
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
let asset = AVURLAsset(url: url)
let duration = CMTimeGetSeconds(asset.duration)
print("duration: \(duration) seconds")
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
generator.maximumSize = CGSize(width: 1100, height: 800)
generator.requestedTimeToleranceBefore = .zero
generator.requestedTimeToleranceAfter = .zero
let count = min(40, max(12, Int(duration * 4)))
for i in 0..<count {
    let seconds = min(duration - 0.03, Double(i) * duration / Double(count))
    do {
        let cg = try generator.copyCGImage(at: CMTime(seconds: seconds, preferredTimescale: 600), actualTime: nil)
        let bitmap = NSBitmapImageRep(cgImage: cg)
        let data = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.9])!
        try data.write(to: output.appendingPathComponent(String(format: "frame-%02d.jpg", i)))
        print(String(format: "%02d %.3f", i, seconds))
    } catch { print("Frame \(i): \(error)") }
}
