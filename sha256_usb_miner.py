#!/usr/bin/env python3
"""
SHA-256 USB Miner Scaffold
Safe USB-aware proof-of-work miner with ledgered audit trails and explicit-run operation.
Educational benchmarking and safe shutdown support.
"""

import hashlib
import time
import sys
import logging
from dataclasses import dataclass
from typing import Optional, Tuple, Any, List, Dict


@dataclass
class MinerConfig:
    """Configuration for SHA-256 miner."""
    difficulty: int = 4
    # Practical default for local testing; override for long runs
    max_nonce: int = 2**24 - 1
    usb_safe: bool = True
    verbose: bool = False


@dataclass
class MineResult:
    """Result of a mining operation."""
    nonce: int
    hash_value: str
    iterations: int
    time_elapsed: float
    difficulty: int


class SHA256Miner:
    """Safe USB-aware SHA-256 proof-of-work miner."""

    def __init__(self, config: Optional[MinerConfig] = None):
        """Initialize miner with optional configuration."""
        self.config = config or MinerConfig()
        self.audit_log: List[Dict[str, Any]] = []
        self._running = False

    def mine(self, data: str, max_iterations: Optional[int] = None) -> MineResult:
        """
        Mine a proof-of-work hash meeting difficulty requirement.

        Args:
            data: Data to mine (text)
            max_iterations: optional early-stop iteration limit for testing

        Returns:
            MineResult with nonce, hash, and metrics
        """
        self._running = True
        start_time = time.time()
        target = "0" * self.config.difficulty

        limit = self.config.max_nonce
        if max_iterations is not None:
            limit = min(limit, max_iterations)

        for nonce in range(limit):
            if not self._running:
                raise RuntimeError("Mining interrupted")

            message = f"{data}{nonce}"
            hash_value = hashlib.sha256(message.encode()).hexdigest()

            if hash_value.startswith(target):
                elapsed = time.time() - start_time
                result = MineResult(
                    nonce=nonce,
                    hash_value=hash_value,
                    iterations=nonce + 1,
                    time_elapsed=elapsed,
                    difficulty=self.config.difficulty,
                )

                self._log_audit(data, result)
                if self.config.verbose:
                    self._log_result(result)

                return result

        raise RuntimeError(f"Failed to find nonce within {limit} iterations")

    def _log_audit(self, data: str, result: MineResult) -> None:
        """Log mining result to audit trail."""
        entry = {
            "timestamp": time.time(),
            "data": data,
            "nonce": result.nonce,
            "hash": result.hash_value,
            "iterations": result.iterations,
            "time_elapsed": result.time_elapsed,
            "difficulty": result.difficulty,
        }
        self.audit_log.append(entry)

    def _log_result(self, result: MineResult) -> None:
        """Log mining result using logging instead of printing to stdout."""
        logging.info("Found nonce: %d", result.nonce)
        logging.info("  Hash: %s", result.hash_value)
        logging.info("  Iterations: %d", result.iterations)
        logging.info("  Time: %.4fs", result.time_elapsed)
        logging.info("  Difficulty: %d", result.difficulty)

    def shutdown(self) -> None:
        """Safe shutdown."""
        self._running = False


def main():
    """Main entry point for miner."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if len(sys.argv) < 2:
        logging.error("Usage: python sha256_usb_miner.py <data> [difficulty]")
        sys.exit(1)

    data = sys.argv[1]
    difficulty = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    config = MinerConfig(difficulty=difficulty, verbose=True)
    miner = SHA256Miner(config)

    try:
        result = miner.mine(data)
        logging.info("\n🏆 Mining successful!")
    except KeyboardInterrupt:
        logging.warning("\n⚠️  Mining interrupted by user")
        miner.shutdown()
    except Exception as e:
        logging.error("\n❌ Mining failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
