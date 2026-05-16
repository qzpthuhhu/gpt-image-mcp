from dataclasses import dataclass
from typing import Optional
import httpx

@dataclass
class ImageResult:
    url: str
    revised_prompt: Optional[str]
    b64_json: Optional[str] = None

class ImageGenerator:
    def __init__(self, api_key: str, base_url: str = "https://api.apiyi.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)

    async def generate(
        self,
        prompt: str,
        model: str = "gpt-image-2",
        n: int = 1,
        size: str = "1024x1024",
    ) -> dict:
        """调用图像生成 API"""
        response = await self.client.post(
            f"{self.base_url}/images/generations",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "prompt": prompt,
                "n": n,
                "size": size,
            },
        )
        response.raise_for_status()
        data = response.json()

        return {
            "images": [
                {
                    "url": img.get("url"),
                    "revised_prompt": img.get("revised_prompt"),
                    "b64_json": img.get("b64_json"),
                }
                for img in data.get("data", [])
            ],
            "model": model,
            "usage": data.get("usage", {}),
        }

    async def close(self):
        await self.client.aclose()