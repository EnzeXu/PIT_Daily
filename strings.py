STRING_MAIL_TEXT_HEAD = """
<html>
<head>
    <style>
    #table_normal table {
        width: 100%;
        margin: 15px 0;
        border: 0;
    }
    #table_normal th {
        background-color: #acd6ff;
        color:#000000
    }
    #table_normal,#table_normal th,#table_normal td {
        font-size: 1.0em;
        text-align: center;
        padding: 4px;
        border-collapse: collapse;
    }
    #table_normal th,#table_normal td {
        border: 1px solid #c4e1ff;
        border-width:1px 0 1px 0
    }
    #table_normal tr {
        border: 1px solid #c4e1ff;
    }
    #table_normal tr:nth-child(odd){
        background-color: #ecf5ff;
    }
    #table_normal tr:nth-child(even){
        background-color: #fdfdfd;
    }

    #table_highlight table {
        width: 100%;
        margin: 15px 0;
        border: 0;
    }
    #table_highlight th {
        background-color: #ff9797;
        color: #000000
    }
    #table_highlight,#table_highlight th,#table_highlight td {
        font-size: 1.0em;
        text-align: center;
        padding: 4px;
        border-collapse: collapse;
    }
    #table_highlight th,#table_highlight td {
        border: 1px solid #ffb5b5;
        border-width: 1px 0 1px 0
    }
    #table_highlight tr {
        border: 1px solid #ffb5b5;
    }
    #table_highlight tr:nth-child(odd){
        background-color: #ffecec;
    }
    #table_highlight tr:nth-child(even){
        background-color: #fdfdfd;
    }
    </style>
</head>
<body>
"""
STRING_MAIL_TEXT_TITLE = """
<h1>PIT Daily [{0}]</h1>
"""

STRING_MAIL_TEXT_README = """
<h2>Details</h2>
<pre style="margin: 15px 0 0 0; padding: 20px; border: 0; border: 1px solid #c4e1ff; background: #ecf5ff; line-height: 1.4; font-family: Consolas; display: block; text-align: left; font-size: 1.0em; width: 1000px">
{0}
{1}
{2}
</pre>
"""

STRING_MAIL_TEXT_TAIL = """
</body>
</html>
"""

STRING_MAIL_TEXT_PART_NORMAL = """
<h2>{0}</h2>
<pre style="margin: 15px 0 0 0; border: 0; line-height: 1.4; font-family: Consolas; display: block; text-align: center;">
{1}
</pre>
"""

STRING_MAIL_TEXT_PART_LOG = """
<h2>{0}</h2>
<pre style="margin: 15px 0 0 0; padding: 20px; border: 0; border: 1px solid #c4e1ff; background: #ecf5ff; line-height: 1.4; font-family: Consolas; display: block; text-align: left; font-size: 1.0em; width: 1000px">
{1}</pre>
"""

STRING_MAIL_TEXT_PART_NONE_BLUE = """
<h2>{0}</h2>
<pre style="margin: 15px 0 0 0; padding: 20px; border: 0; border: 1px solid #c4e1ff; background: #ecf5ff; line-height: 1.4; font-family: Consolas; display: block; text-align: left; font-size: 1.0em; width: 1000px">
{1}</pre>
"""

STRING_MAIL_TEXT_PART_NONE_RED = """
<h2>{0}</h2>
<pre style="margin: 15px 0 0 0; padding: 20px; border: 0; border: 1px solid #ffb5b5; background: #ffecec; line-height: 1.4; font-family: Consolas; display: block; text-align: left; font-size: 1.0em; width: 1000px">
{1}</pre>
"""