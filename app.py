# app.py

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import time
import sys
import os

class Meta(Enum):
    AI = "AI/Tech"
    ANIMALS = "Animals"
    VIRAL = "Viral/Memes"
    GAMING = "Gaming"
    CELEBRITY = "Celebrity"
    SPORTS = "Sports"
    POLITICS = "Politics"

class ScanStrategy(Enum):
    MICRO_CAP = "50K_OR_LESS"
    SMALL_CAP = "100K_OR_LESS"
    MID_CAP = "3M_OR_LESS"
    DIP_HUNTING = "BUYING_DIPS"

class MetaTracker:
    def __init__(self):
        self.current_metas = {
            Meta.AI: {
                "score": 100,
                "keywords": ["ai", "gpt", "bot", "agent", "neural", "brain", "intelligence", "machine", "compute"],
                "volume_24h": 0,
                "recent_pairs": []
            },
            Meta.ANIMALS: {
                "score": 85,
                "keywords": ["cat", "dog", "hippo", "monkey", "frog", "bird", "animal", "zoo", "pet"],
                "volume_24h": 0,
                "recent_pairs": []
            },
            Meta.VIRAL: {
                "score": 80,
                "keywords": ["meme", "viral", "tiktok", "trend", "viral", "internet", "social"],
                "volume_24h": 0,
                "recent_pairs": []
            },
            Meta.GAMING: {
                "score": 75,
                "keywords": ["game", "play", "minecraft", "quest", "gaming", "player", "console"],
                "volume_24h": 0,
                "recent_pairs": []
            }
        }
        self.momentum_window = timedelta(hours=24)

    def update_meta(self, pair: Dict):
        """Update meta stats based on new pair data"""
        name = pair.get('baseToken', {}).get('name', '').lower()
        symbol = pair.get('baseToken', {}).get('symbol', '').lower()
        volume_24h = float(pair.get('volume', {}).get('h24', 0) or 0)

        for meta, data in self.current_metas.items():
            if any(kw in name or kw in symbol for kw in data["keywords"]):
                data["volume_24h"] += volume_24h
                data["recent_pairs"].append({
                    "name": name,
                    "symbol": symbol,
                    "volume": volume_24h,
                    "timestamp": datetime.now()
                })

                # Clean old data
                data["recent_pairs"] = [
                    p for p in data["recent_pairs"]
                    if datetime.now() - p["timestamp"] < self.momentum_window
                ]

    def get_hot_metas(self) -> List[tuple[Meta, float]]:
        """Get currently trending metas sorted by momentum"""
        momentum_scores = {}
        for meta, data in self.current_metas.items():
            recent_volume = sum(p["volume"] for p in data["recent_pairs"])
            pair_count = len(data["recent_pairs"])
            momentum = (recent_volume * 0.7 + (pair_count * 100000) * 0.3) * (data["score"] / 100)
            momentum_scores[meta] = momentum

        return sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    
class WhaleKOLTracker:
    def __init__(self):
            self.whale_wallets = {
                "HN4AkYD4N6f4KFYkxFemY6bz2B3qubGtK1r6H3ymYAFS": {
                    "name": "Known Whale 1",
                    "type": "whale",
                    "tags": ["AI trader", "Early adopter"],
                    "success_rate": 0.85,
                    "last_trades": [],
                    "total_volume": 0
                }
            }
            
            self.kol_wallets = {
                "2MxyVwqWGbsB6RhQvfNQrfEKyDr9fLt2Z5FxQs5vRECF": {
                    "name": "KOL 1",
                    "type": "kol",
                    "tags": ["Meme specialist", "High influence"],
                    "followers": 50000,
                    "success_rate": 0.92,
                    "last_calls": []
                }
            }
            
    def add_whale_wallet(self, address: str, name: str, tags: List[str] = None) -> bool:
            """Add a new whale wallet to track"""
            try:
                self.whale_wallets[address] = {
                    "name": name,
                    "type": "whale",
                    "tags": tags or [],
                    "success_rate": 0.0,
                    "last_trades": [],
                    "total_volume": 0,
                    "added_date": datetime.now()
                }
                print(f"Added whale wallet: {name} ({address})")
                return True
            except Exception as e:
                print(f"Error adding whale wallet: {e}")
                return False
                
    def add_kol_wallet(self, address: str, name: str, followers: int, tags: List[str] = None) -> bool:
        """Add a new KOL wallet to track"""
        try:
            self.kol_wallets[address] = {
                "name": name,
                "type": "kol",
                "tags": tags or [],
                "followers": followers,
                "success_rate": 0.0,
                "last_calls": [],
                "added_date": datetime.now()
            }
            print(f"Added KOL wallet: {name} ({address})")
            return True
        except Exception as e:
            print(f"Error adding KOL wallet: {e}")
            return False

    def analyze_wallet_interest(self, pair: Dict) -> Dict:
            """Analyze whale and KOL interest in a token"""
            try:
                liquidity = float(pair.get('liquidity', {}).get('usd', 0) or 0)
                volume_24h = float(pair.get('volume', {}).get('h24', 0) or 0)
                contract = pair.get('baseToken', {}).get('address', '')
                
                # Check for whale activity
                whale_score = 0
                active_whales = []
                for address, whale in self.whale_wallets.items():
                    if self._check_wallet_activity(address, contract):
                        whale_score += whale['success_rate'] * 20
                        active_whales.append(whale['name'])
                
                # Check for KOL interest
                kol_score = 0
                active_kols = []
                for address, kol in self.kol_wallets.items():
                    if self._check_wallet_activity(address, contract):
                        influence_factor = min(kol['followers'] / 10000, 10)
                        kol_score += kol['success_rate'] * influence_factor * 10
                        active_kols.append(kol['name'])
                
                # Combined analysis
                combined_score = (whale_score * 0.6 + kol_score * 0.4)
                risk_level = self._assess_risk_level(combined_score, len(active_whales), len(active_kols))
                
                return {
                    'score': min(100, combined_score),
                    'whale_metrics': {
                        'active_whales': active_whales,
                        'whale_score': whale_score
                    },
                    'kol_metrics': {
                        'active_kols': active_kols,
                        'kol_score': kol_score
                    },
                    'risk_level': risk_level
                }
                
            except Exception as e:
                print(f"Error in wallet analysis: {e}")
                return {

                    'score': 0,
                    'whale_metrics': {'active_whales': [], 'whale_score': 0},
                    'kol_metrics': {'active_kols': [], 'kol_score': 0},
                    'risk_level': 'high'
                }
    
    def _check_wallet_activity(self, wallet_address: str, token_address: str) -> bool:
        """Check if wallet has recent activity with token"""
        # This would need to be implemented with actual blockchain data
        return False

    def _assess_risk_level(self, score: float, whale_count: int, kol_count: int) -> str:
        """Assess risk level based on wallet activity"""
        if score >= 80 and whale_count >= 2:
            return "low"
        elif score >= 60 and (whale_count >= 1 or kol_count >= 2):
            return "medium"
        elif score < 30 or (whale_count == 0 and kol_count == 0):
            return "high"
        else:
            return "medium"

    def get_wallet_stats(self) -> Dict:
        """Get current wallet statistics"""
        return {
            'whales': {
                'count': len(self.whale_wallets),
                'avg_success_rate': sum(w['success_rate'] for w in self.whale_wallets.values()) / len(self.whale_wallets) if self.whale_wallets else 0
            },
            'kols': {
                'count': len(self.kol_wallets),
                'total_followers': sum(k['followers'] for k in self.kol_wallets.values()),
                'avg_success_rate': sum(k['success_rate'] for k in self.kol_wallets.values()) / len(self.kol_wallets) if self.kol_wallets else 0
            }
        }   
class JupiterTrader:

    def __init__(self):
        self.referral_key = "6svoeECRFJvcazjUMbF4axe6Qp55MNm8FB8CkVXjYUqB"
        self.fees_bps = "50"
        self.base_url = "https://jup.ag"

    def get_trade_link(self, token_address: str, token_symbol: str) -> str:
        """Generate Jupiter trading link with referral"""
        return (
            f"{self.base_url}/swap/{token_symbol}-SOL"
            f"?referrer={self.referral_key}&feeBps={self.fees_bps}"
        )

    def get_quick_links(self, token_data: Dict) -> Dict[str, str]:
        """Generate all relevant trading and info links"""
        token_address = token_data.get('contract', '')
        token_symbol = token_data.get('token_symbol', '')

        return {
            'jupiter': self.get_trade_link(token_address, token_symbol),
            'dexscreener': token_data.get('url', ''),
            'solscan': f"https://solscan.io/token/{token_address}"
        }

class MemecoinScanner:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex/search"
        self.meta_tracker = MetaTracker()
        self.wallet_tracker = WhaleKOLTracker()
        self.jupiter_trader = JupiterTrader()
        
    def add_whale(self, address: str, name: str, tags: List[str] = None) -> bool:
        """Add a new whale wallet to track"""
        return self.wallet_tracker.add_whale_wallet(address, name, tags)

    def add_kol(self, address: str, name: str, followers: int, tags: List[str] = None) -> bool:
        """Add a new KOL wallet to track"""
        return self.wallet_tracker.add_kol_wallet(address, name, followers, tags)

    def search_pairs(self, query: str = "solana") -> List[Dict]:
        """Search pairs using DEXScreener API"""
        try:
            params = {"q": query}
            response = requests.get(self.base_url, params=params)

            if response.status_code != 200:
                print(f"Error searching pairs: Status {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return []

            data = response.json()
            pairs = data.get('pairs', [])

            # Filter for Solana pairs
            solana_pairs = [p for p in pairs if p.get('chainId') == 'solana']
            print(f"Found {len(solana_pairs)} Solana pairs for query: {query}")

            # Update meta tracking
            for pair in solana_pairs:
                self.meta_tracker.update_meta(pair)

            return solana_pairs

        except Exception as e:
            print(f"Error in search_pairs: {e}")
            return []

    def filter_pairs(self, pairs: List[Dict], strategy: ScanStrategy) -> List[Dict]:
        """Filter pairs based on strategy criteria"""
        filtered = []

        for pair in pairs:
            try:
                liquidity = float(pair.get('liquidity', {}).get('usd', 0) or 0)
                volume_24h = float(pair.get('volume', {}).get('h24', 0) or 0)
                fdv = float(pair.get('fdv', 0) or 0)

                # Skip pairs with invalid metrics
                if liquidity == 0 or volume_24h == 0 or fdv == 0:
                    continue

                meets_criteria = False

                if strategy == ScanStrategy.MICRO_CAP:
                    meets_criteria = (
                        liquidity >= 10000 and
                        volume_24h >= 30000 and
                        50000 <= fdv <= 20000000
                    )

                elif strategy == ScanStrategy.SMALL_CAP:
                    meets_criteria = (
                        liquidity >= 10000 and
                        volume_24h >= 30000 and
                        100000 <= fdv <= 20000000
                    )

                elif strategy == ScanStrategy.MID_CAP:
                    meets_criteria = (
                        liquidity >= 10000 and
                        volume_24h >= 3000000 and
                        1000000 <= fdv <= 3000000
                    )

                elif strategy == ScanStrategy.DIP_HUNTING:
                    price_change_24h = float(pair.get('priceChange', {}).get('h24', 0) or 0)
                    meets_criteria = (
                        liquidity >= 10000 and
                        volume_24h >= 300000 and
                        100000 <= fdv <= 10000000 and
                        price_change_24h < -10
                    )

                if meets_criteria:
                    # Add whale/KOL analysis
                    wallet_analysis = self.wallet_tracker.analyze_wallet_interest(pair)
                    pair['wallet_analysis'] = wallet_analysis
                    filtered.append(pair)

            except Exception as e:
                continue

        # Sort by volume
        return sorted(
            filtered,
            key=lambda x: float(x.get('volume', {}).get('h24', 0) or 0),
            reverse=True
        )

    def format_pair_info(self, pair: Dict) -> Dict:
        """Format pair information for display"""
        try:
            # Basic info
            formatted_info = {
                'token_name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'token_symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'price_usd': float(pair.get('priceUsd', 0) or 0),
                'price_change': {
                    '5m': float(pair.get('priceChange', {}).get('m5', 0) or 0),
                    '1h': float(pair.get('priceChange', {}).get('h1', 0) or 0),
                    '6h': float(pair.get('priceChange', {}).get('h6', 0) or 0),
                    '24h': float(pair.get('priceChange', {}).get('h24', 0) or 0)
                },
                'liquidity': float(pair.get('liquidity', {}).get('usd', 0) or 0),
                'volume': {
                    '24h': float(pair.get('volume', {}).get('h24', 0) or 0)
                },
                'fdv': float(pair.get('fdv', 0) or 0),
                'dex': pair.get('dexId', 'Unknown'),
                'pair_address': pair.get('pairAddress', 'Unknown'),
                'contract': pair.get('baseToken', {}).get('address', 'Unknown'),
                'url': pair.get('url', '')
            }

            # Add whale/KOL analysis if available
            wallet_analysis = pair.get('wallet_analysis', {})
            if wallet_analysis:
                formatted_info['wallet_analysis'] = wallet_analysis

            # Add trading links
            formatted_info['links'] = self.jupiter_trader.get_quick_links(formatted_info)

            return formatted_info

        except Exception as e:
            print(f"Error formatting pair info: {e}")
            return {}

    def get_tracker_stats(self) -> Dict:
        """Get current tracker statistics"""
        return self.wallet_tracker.get_wallet_stats()

def format_number(num: float) -> str:
    """Format numbers for display"""
    try:
        if num >= 1_000_000:
            return f"${num/1_000_000:.2f}M"
        elif num >= 1_000:
            return f"${num/1_000:.2f}K"
        return f"${num:.2f}"
    except Exception:
        return "N/A"

def main():
    try:
        scanner = MemecoinScanner()
        print("\n🔍 Solana Memecoin Scanner v5.2\n")

        # Example of adding new wallets
        scanner.add_whale(
            "ABC123DefExample...", 
            "New Whale",
            tags=["AI trader", "High volume"]
        )
        
        scanner.add_kol(
            "XYZ789KolExample...",
            "Crypto Influencer",
            followers=75000,
            tags=["Meme expert", "Early caller"]
        )

        # Get current meta trends
        hot_metas = scanner.meta_tracker.get_hot_metas()
        print("Current Hot Metas:")
        for meta, score in hot_metas:
            print(f"- {meta.value}: {score:.1f}")
        print()

        # Display tracker stats
        stats = scanner.get_tracker_stats()
        print("\nTracker Statistics:")
        print(f"Active Whales: {stats['whales']['count']}")
        print(f"Average Whale Success Rate: {stats['whales']['avg_success_rate']:.2%}")
        print(f"Active KOLs: {stats['kols']['count']}")
        print(f"Total KOL Followers: {stats['kols']['total_followers']:,}")
        print()

        # Search terms combining current metas and basic searches
        search_terms = [
            "solana meme",
            "sol dog",
            "sol cat",
            "solana ai",
            "solana new",
            "raydium new"
        ]

        # Add terms based on hot metas
        for meta, _ in hot_metas[:3]:
            search_terms.append(f"solana {meta.value.lower()}")

        all_pairs = []
        for term in search_terms:
            print(f"\nSearching: {term}")
            pairs = scanner.search_pairs(term)
            all_pairs.extend(pairs)

        # Remove duplicates
        unique_pairs = {
            pair.get('pairAddress'): pair 
            for pair in all_pairs 
            if pair.get('pairAddress')
        }

        print(f"\nFound {len(unique_pairs)} unique pairs")

        # Process each strategy
        for strategy in ScanStrategy:
            print(f"\nProcessing {strategy.value}...")
            filtered_pairs = scanner.filter_pairs(list(unique_pairs.values()), strategy)

            if filtered_pairs:
                print(f"\n=== {strategy.value} ===")
                for idx, pair in enumerate(filtered_pairs[:20], 1):
                    info = scanner.format_pair_info(pair)
                    if not info:
                        continue

                    print(f"\n#{idx} {info['token_name']} (${info['token_symbol']})")
                    print(f"Price: {format_number(info['price_usd'])}")
                    print(f"FDV: {format_number(info['fdv'])}")
                    print(f"Liquidity: {format_number(info['liquidity'])}")
                    print(f"Volume 24h: {format_number(info['volume']['24h'])}")

                    print(f"Price Changes:")
                    print(f"  5m: {info['price_change']['5m']:.1f}%")
                    print(f"  1h: {info['price_change']['1h']:.1f}%")
                    print(f"  6h: {info['price_change']['6h']:.1f}%")
                    print(f"  24h: {info['price_change']['24h']:.1f}%")

                    # Whale/KOL Analysis
                    if 'wallet_analysis' in info:
                        analysis = info['wallet_analysis']
                        print("\nWhale/KOL Analysis:")
                        print(f"  Score: {analysis['score']:.1f}")
                        print(f"  Risk Level: {analysis['risk_level'].upper()}")
                        
                        if analysis['whale_metrics']['active_whales']:
                            print(f"  Active Whales: {', '.join(analysis['whale_metrics']['active_whales'])}")
                        
                        if analysis['kol_metrics']['active_kols']:
                            print(f"  Active KOLs: {', '.join(analysis['kol_metrics']['active_kols'])}")

                    print("\nQuick Links:")
                    print(f"Trade (Jupiter): {info['links']['jupiter']}")
                    print(f"DexScreener: {info['links']['dexscreener']}")
                    print(f"Solscan: {info['links']['solscan']}")
                    print("-" * 80)
            else:
                print(f"\nNo results found for {strategy.value}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScanner stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
