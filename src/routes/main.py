from fastapi import APIRouter
from starlette.responses import HTMLResponse
import asyncio
import discord


# APIRouter is equivalent to Flask's blueprint
# It allows us to extend FastAPI Routes
router = APIRouter()

@router.get("/")
def main():
    """
    Displays Pan's News Feed
    :return: HTMLResponse - Pan's News Feed
    """

    title = """
    <pre>
########     ###    ##    ## ####  ######     ##    ## ######## ##      ##  ######     ######## ######## ######## ########     
##     ##   ## ##   ###   ## #### ##    ##    ###   ## ##       ##  ##  ## ##    ##    ##       ##       ##       ##     ##    
##     ##  ##   ##  ####  ##  ##  ##          ####  ## ##       ##  ##  ## ##          ##       ##       ##       ##     ##    
########  ##     ## ## ## ## ##    ######     ## ## ## ######   ##  ##  ##  ######     ######   ######   ######   ##     ##    
##        ######### ##  ####            ##    ##  #### ##       ##  ##  ##       ##    ##       ##       ##       ##     ##    
##        ##     ## ##   ###      ##    ##    ##   ### ##       ##  ##  ## ##    ##    ##       ##       ##       ##     ##    
##        ##     ## ##    ##       ######     ##    ## ########  ###  ###   ######     ##       ######## ######## ########  
    </pre>             
                                                                      
    """
        
    return HTMLResponse(title)


@router.get("/health")
def health():
    """
    Displays a health check
    :return: HTMLResponse - Pan's News Feed
    """

    health = "healthy"

    return HTMLResponse(health)


