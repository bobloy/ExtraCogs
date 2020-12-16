from .dune import Dune


async def setup(bot):
    bot.add_cog(Dune(bot))
