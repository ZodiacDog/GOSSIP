#!/usr/bin/env python3
"""
Gossip - Universal AI System Integration Layer
Command-line tool and library for creating portable AI conversation contexts

Gossip enables seamless context transfer between different AI systems, solving
the fundamental interoperability problem in AI conversations.

Usage:
    python gossip.py create --topic "My Topic" --summary "..." 
    python gossip.py resume gossip_file.gossip --target chatgpt
    
Or import as a library:
    from gossip import Gossip
    g = Gossip(topic="My Topic", summary="...")
    g.save("conversation.gossip")

System Integration Features:
    - Cross-platform AI compatibility
    - Universal context format
    - File attachment support
    - Automated compression
    - API-ready structure
"""

import json
import base64
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import uuid


class Gossip:
    """
    Represents a portable AI conversation context that enables system integration
    and seamless transfer between different AI platforms.
    
    This class implements the Gossip format - a universal integration layer for
    AI conversations that preserves context, reasoning, and continuity across
    different AI systems (Claude, ChatGPT, Gemini, Grok, etc.).
    """
    
    VERSION = "1.0"
    
    def __init__(
        self,
        topic: str,
        summary: str,
        source_ai: str = "unknown",
        key_points: Optional[List[str]] = None,
        open_questions: Optional[List[str]] = None,
        continuation: Optional[str] = None,
        gossip_id: Optional[str] = None,
        created: Optional[str] = None
    ):
        """
        Initialize a Gossip conversation context.
        
        Args:
            topic: Conversation topic/title
            summary: Comprehensive conversation summary with reasoning
            source_ai: Source AI system (claude, chatgpt, gemini, grok, other)
            key_points: List of key decisions and facts
            open_questions: List of unresolved topics
            continuation: Next instruction for AI
            gossip_id: Unique identifier (auto-generated if not provided)
            created: ISO timestamp (auto-generated if not provided)
        """
        self.gossip_id = gossip_id or f"gossip_{uuid.uuid4().hex[:12]}"
        self.created = created or datetime.utcnow().isoformat() + "Z"
        
        self.metadata = {
            "topic": topic,
            "source_ai": source_ai,
            "created_by": "Gossip v1.0"
        }
        
        self.context = {
            "summary": summary,
            "key_points": key_points or [],
            "open_questions": open_questions or []
        }
        
        self.files: List[Dict[str, Any]] = []
        self.continuation = continuation or ""
    
    def add_file(self, filepath: str) -> None:
        """
        Add a file to the Gossip context (base64 encoded for portability).
        
        This enables file attachments to travel with the conversation context
        across different AI systems.
        
        Args:
            filepath: Path to file to attach
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            data = f.read()
            encoded = base64.b64encode(data).decode('utf-8')
        
        mime_type = self._get_mime_type(path.suffix)
        
        self.files.append({
            "name": path.name,
            "type": mime_type,
            "size": len(data),
            "encoding": "base64",
            "data": encoded
        })
        
        print(f"✅ File attached: {path.name} ({len(data)/1024:.1f} KB)")
    
    def _get_mime_type(self, extension: str) -> str:
        """Detect MIME type from file extension."""
        mime_map = {
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.csv': 'text/csv',
            '.md': 'text/markdown',
            '.py': 'text/x-python',
            '.js': 'text/javascript',
            '.html': 'text/html',
            '.xml': 'text/xml',
            '.zip': 'application/zip',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }
        return mime_map.get(extension.lower(), 'application/octet-stream')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Gossip to dictionary for JSON serialization."""
        return {
            "version": self.VERSION,
            "gossip_id": self.gossip_id,
            "created": self.created,
            "metadata": self.metadata,
            "context": self.context,
            "files": self.files,
            "continuation": self.continuation
        }
    
    def to_json(self, pretty: bool = True) -> str:
        """
        Convert Gossip to JSON string.
        
        Args:
            pretty: If True, format with indentation
            
        Returns:
            JSON string representation
        """
        indent = 2 if pretty else None
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_human_readable(self) -> str:
        """
        Generate human-readable Gossip format optimized for direct AI input.
        
        This format is designed to be copy-pasted directly into any AI chat
        interface, providing complete context for seamless continuation.
        
        Returns:
            Formatted string ready for AI consumption
        """
        lines = [
            f"# GOSSIP [ID: {self.gossip_id}]",
            "═" * 63,
            "AI Conversation Context Transfer File",
            "Created by Gossip - Universal AI Integration Layer",
            "═" * 63,
            "",
            f"**Topic:** {self.metadata['topic']}",
            f"**Source AI:** {self.metadata['source_ai']}",
            f"**Created:** {datetime.fromisoformat(self.created.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "═" * 63,
            "## CONVERSATION CONTEXT",
            "",
            self.context['summary'],
            "",
            "═" * 63,
            "## KEY POINTS & DECISIONS",
            ""
        ]
        
        for point in self.context['key_points']:
            lines.append(f"• {point.lstrip('- ')}")
        
        lines.extend([
            "",
            "═" * 63,
            "## OPEN QUESTIONS / NEXT STEPS",
            ""
        ])
        
        for question in self.context['open_questions']:
            lines.append(f"• {question.lstrip('- ')}")
        
        if self.files:
            lines.extend([
                "",
                "═" * 63,
                "## ATTACHED FILES",
                ""
            ])
            for file in self.files:
                size_kb = file['size'] / 1024
                lines.append(f"• {file['name']} ({file['type']}, {size_kb:.1f} KB)")
            lines.extend([
                "",
                "[Files are base64-encoded in the full Gossip JSON format]"
            ])
        
        if self.continuation:
            lines.extend([
                "",
                "═" * 63,
                "## CONTINUE FROM HERE:",
                "",
                self.continuation
            ])
        
        lines.extend([
            "",
            "═" * 63,
            "## INSTRUCTIONS FOR AI SYSTEMS:",
            "",
            "This is a Gossip file - a universal context transfer format for AI systems.",
            f"Please read this entire context carefully. This represents a conversation",
            f"from another AI system ({self.metadata['source_ai']}) that should continue",
            "seamlessly in your system.",
            "",
            "Treat this as if you've been having this conversation yourself. Reference",
            "the key points and decisions made, acknowledge the open questions, and pick",
            "up from the 'Continue from here' section.",
            "",
            "If files are referenced but not accessible in your system, acknowledge them",
            "and proceed based on the context provided.",
            "",
            "Gossip enables AI interoperability. Honor the context and maintain continuity.",
            "═" * 63
        ])
        
        return "\n".join(lines)
    
    def save(self, filepath: str, format: str = "json") -> None:
        """
        Save Gossip to file.
        
        Args:
            filepath: Output file path
            format: 'json' for .gossip files or 'txt' for human-readable
        """
        path = Path(filepath)
        
        if format == "json":
            content = self.to_json(pretty=True)
            if not str(path).endswith('.gossip') and not str(path).endswith('.json'):
                path = path.with_suffix('.gossip')
        elif format == "txt":
            content = self.to_human_readable()
            if not str(path).endswith('.txt'):
                path = path.with_suffix('.txt')
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        size_kb = len(content.encode('utf-8')) / 1024
        print(f"✅ Gossip saved: {path} ({size_kb:.1f} KB)")
    
    @classmethod
    def load(cls, filepath: str) -> 'Gossip':
        """
        Load Gossip from file.
        
        Args:
            filepath: Path to .gossip or .txt file
            
        Returns:
            Gossip instance
            
        Raises:
            ValueError: If file cannot be parsed
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            data = json.loads(content)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            raise ValueError("Could not parse Gossip file. Ensure it's valid JSON format.")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Gossip':
        """Create Gossip instance from dictionary."""
        gossip = cls(
            topic=data['metadata']['topic'],
            summary=data['context']['summary'],
            source_ai=data['metadata'].get('source_ai', 'unknown'),
            key_points=data['context'].get('key_points', []),
            open_questions=data['context'].get('open_questions', []),
            continuation=data.get('continuation', ''),
            gossip_id=data['gossip_id'],
            created=data['created']
        )
        gossip.files = data.get('files', [])
        return gossip
    
    def generate_resume_prompt(self, target_ai: str = "universal") -> str:
        """
        Generate AI-optimized resume prompt for target system.
        
        This creates a prompt optimized for the specific AI platform,
        enabling seamless integration and context continuation.
        
        Args:
            target_ai: Target AI system (universal, claude, chatgpt, gemini, grok)
            
        Returns:
            Optimized prompt string for the target AI
        """
        base_prompt = self.to_human_readable()
        
        optimizations = {
            'claude': '\n\n[Gossip Integration Note for Claude: This context comes from another AI system. Please maintain the analytical depth and reasoning quality established in the original conversation.]',
            'chatgpt': '\n\n[Gossip Integration Note for ChatGPT: Continue this conversation with the same level of detail and context awareness as the original AI system.]',
            'gemini': '\n\n[Gossip Integration Note for Gemini: This is a Gossip context transfer from another AI. Please continue seamlessly from where the previous system left off.]',
            'grok': '\n\n[Gossip Integration Note for Grok: Picking up from another AI via Gossip. Keep the same energy and depth.]',
            'universal': ''
        }
        
        return base_prompt + optimizations.get(target_ai, optimizations['universal'])
    
    def extract_file(self, filename: str, output_path: Optional[str] = None) -> str:
        """
        Extract attached file from Gossip.
        
        Args:
            filename: Name of file to extract
            output_path: Optional output path (defaults to filename)
            
        Returns:
            Path where file was extracted
            
        Raises:
            ValueError: If file not found in Gossip
        """
        for file in self.files:
            if file['name'] == filename:
                data = base64.b64decode(file['data'])
                
                if output_path is None:
                    output_path = filename
                
                with open(output_path, 'wb') as f:
                    f.write(data)
                
                print(f"✅ Extracted: {output_path} ({len(data)/1024:.1f} KB)")
                return output_path
        
        raise ValueError(f"File not found in Gossip: {filename}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get Gossip statistics and metadata.
        
        Returns:
            Dictionary with size, file count, and other metrics
        """
        json_size = len(self.to_json(pretty=False))
        human_size = len(self.to_human_readable())
        
        return {
            "gossip_id": self.gossip_id,
            "topic": self.metadata['topic'],
            "created": self.created,
            "source_ai": self.metadata['source_ai'],
            "key_points_count": len(self.context['key_points']),
            "open_questions_count": len(self.context['open_questions']),
            "files_count": len(self.files),
            "total_file_size_kb": sum(f['size'] for f in self.files) / 1024,
            "json_size_kb": json_size / 1024,
            "human_readable_size_kb": human_size / 1024,
            "compression_ratio": f"{(human_size / json_size * 100):.1f}%" if json_size > 0 else "N/A"
        }


def main():
    """Command-line interface for Gossip."""
    parser = argparse.ArgumentParser(
        description="Gossip - Universal AI System Integration Layer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Create a Gossip file:
    python gossip.py create --topic "AI Ethics" --summary "Discussed..." --output conversation.gossip
  
  Resume from Gossip file:
    python gossip.py resume conversation.gossip --target claude
  
  View Gossip information:
    python gossip.py info conversation.gossip
  
  Extract file from Gossip:
    python gossip.py extract conversation.gossip document.pdf
    
System Integration:
  Gossip enables seamless context transfer between AI systems (Claude, ChatGPT,
  Gemini, Grok). Create portable conversation contexts that work everywhere.
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new Gossip file')
    create_parser.add_argument('--topic', required=True, help='Conversation topic')
    create_parser.add_argument('--summary', required=True, help='Conversation summary')
    create_parser.add_argument('--source-ai', default='unknown', help='Source AI system')
    create_parser.add_argument('--keypoints', help='Key points (comma-separated)')
    create_parser.add_argument('--questions', help='Open questions (comma-separated)')
    create_parser.add_argument('--continuation', help='Next instruction')
    create_parser.add_argument('--files', nargs='+', help='Files to attach')
    create_parser.add_argument('--output', required=True, help='Output file path')
    create_parser.add_argument('--format', choices=['json', 'txt'], default='json', help='Output format')
    
    # Resume command
    resume_parser = subparsers.add_parser('resume', help='Generate resume prompt from Gossip')
    resume_parser.add_argument('gossip', help='Gossip file path')
    resume_parser.add_argument('--target', choices=['universal', 'claude', 'chatgpt', 'gemini', 'grok'],
                               default='universal', help='Target AI system')
    resume_parser.add_argument('--output', help='Output file for resume prompt (optional)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show Gossip information')
    info_parser.add_argument('gossip', help='Gossip file path')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract file from Gossip')
    extract_parser.add_argument('gossip', help='Gossip file path')
    extract_parser.add_argument('filename', help='Name of file to extract')
    extract_parser.add_argument('--output', help='Output path (optional)')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        keypoints = [kp.strip() for kp in args.keypoints.split(',')] if args.keypoints else []
        questions = [q.strip() for q in args.questions.split(',')] if args.questions else []
        
        gossip = Gossip(
            topic=args.topic,
            summary=args.summary,
            source_ai=args.source_ai,
            key_points=keypoints,
            open_questions=questions,
            continuation=args.continuation
        )
        
        if args.files:
            for filepath in args.files:
                try:
                    gossip.add_file(filepath)
                except Exception as e:
                    print(f"⚠️  Could not add file {filepath}: {e}")
        
        gossip.save(args.output, format=args.format)
        
        print("\n🎉 Gossip created successfully!")
        print("This file can now be used with any AI system for seamless context transfer.")
    
    elif args.command == 'resume':
        gossip = Gossip.load(args.gossip)
        resume_prompt = gossip.generate_resume_prompt(args.target)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(resume_prompt)
            print(f"✅ Resume prompt saved to: {args.output}")
        else:
            print("\n" + "="*70)
            print("RESUME PROMPT - Copy and paste into target AI system:")
            print("="*70 + "\n")
            print(resume_prompt)
            print("\n" + "="*70)
    
    elif args.command == 'info':
        gossip = Gossip.load(args.gossip)
        stats = gossip.get_stats()
        
        print("\n📊 Gossip Information:")
        print("=" * 60)
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            print(f"{formatted_key:.<40} {value}")
        print("=" * 60)
        print("\n💡 This Gossip file enables AI system integration")
        print(f"   Source: {gossip.metadata['source_ai']}")
        print(f"   Topic: {gossip.metadata['topic']}")
        print(f"   Compatible with: All major AI systems\n")
    
    elif args.command == 'extract':
        gossip = Gossip.load(args.gossip)
        output_path = gossip.extract_file(args.filename, args.output)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
