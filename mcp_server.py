from mcp.server.fastmcp import FastMCP
from backend.run import run

mcp = FastMCP("AutoC")


@mcp.tool()
def analyze_security_blog(url: str) -> str:
    """
    Analyze a security blog post and extract IoCs, keywords, and Q&A.
    Args:
        url (str): The URL of the blog post to analyze.
    Returns:
        str: The analysis result, including detected keywords, Q&A, and IoCs.
    """
    try:
        res = run(url=url)

        output = ""
        keywords = res.get("keywords_found")
        qna = res.get("qna")
        iocs = res.get("iocs_found")

        # Keywords
        output += f"\n🔍 DETECTED Keywords ({len(keywords)})\n"
        if keywords:
            tags = ", ".join(f"{keyword}" for keyword in keywords)
            output += tags + "\n"
        else:
            output += "No keywords found\n"

        # Q&A
        output += f"\n📝 Q&A about the blog\n"
        if qna:
            for item in qna:
                output += f"Q: {item['question']}\nA: {item['answer']}\n"
        else:
            output += "No Q&A found\n"

        # IoCs
        output += f"\n⚠️ DETECTED IoCs ({len(iocs)})\n"
        if iocs:
            for ioc in iocs:
                output += f"Type: {ioc['type']}, Value: {ioc['value']}\n"
        else:
            output += "No IoCs found\n"
        return output

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport='stdio')
