from fastapi import APIRouter
import requests
from mailjet_rest import Client
import textwrap

api = APIRouter(
    prefix="/emailsapi",
    tags=["emailsapi"],
    responses={404: {"message": "Request for a valid email resource"}}
)


# list of blacklisted emails
blacklisted_emails = [
    "1decision@gmail.com",
    "jufangwang@hotmail.com",
    "jhbailey0802@aol.com",
    "life2021@aol.com",
    "diedra4444@aol.com",
    "demikaki@aol.com",
    "foxgurl118@aol.com",
    "giants2979@aol.com",
    "tadpole31@aol.com",
    "mariekozlowski@aol.com",
    "life2021",
]


# check if email is not blacklisted
async def is_not_blacklisted(email):
    return email not in blacklisted_emails


# list of spam words
async def spam_dictionary():
    return ['hacked', 'databases', 'vulnerability', 'exploit', 'credentials', 'server', 'systematically', 'leaked', 'blackhat', 'bitcoins', 'bitcoin', '1Q1DF9rJS6fNDSpiV2iEA46BS1mNEaELtC', 'leak', 'cex.io', 'reputation', 'anonymous', 'complied', 'hoax', 'bidder', 'DECISIONS', 'FREESPINS', 'boost', 'sales', 'ranks', 'score', 'dofollow', 'backlinks', 'linkbase', 'nofollow', 'SEO', 'hire', 'advertising', 'advertise', 'online', 'Clever', 'rich', 'betting', 'software', 'widget', 'demo', 'proven', 'financing', 'Entrepreneur', 'finance', 'metrics', 'organically', 'whitehat', 'Internet', 'leads', 'traffic', 'Adwords', 'keywords', 'targeted', 'niche', 'blogger', 'awareness', 'clicks', 'growth', 'unsubscribe', 'Trend', 'extra', 'earn', 'sale', 'optimized', 'Financial', 'Boost', 'ranking', 'increase', 'partnership', 'loans', 'PREPAYMENT', 'bet', 'Download', 'argument', 'essay', 'writer', 'essaytyper', 'helper', 'essaybot', 'dissertation', 'welcome', 'likes', 'followers']


# check if email is spam_dictionary
async def is_not_spam(test_string):
    res = any(word in test_string for word in await spam_dictionary())
    return not res


# check if email actually exists / can receive mail
async def is_valid(email):
    # validate mail using https://isitarealemail.com

    # api key
    api_key = "1c96ceb8-36cf-4213-92a5-c66316a3b717"

    # validate email using api
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params={'email': email},
        headers={'Authorization': "Bearer " + api_key})

    # validity of email
    status = response.json()['status']

    """ # expected response and meaning
    if status == "valid":
        print("email is valid")
    elif status == "invalid":
        print("email is invalid")
    else:
        print("email was unknown")
    """
    return status == "valid"


# generate stock request notification email
async def notification_template(notification):
    styles = """
    <style type="text/css">
        table, td {
            color: #000000;
        }

        a {
            color: #38389b;
            text-decoration: underline;
        }

        @media only screen and (min-width: 620px) {
            .u-row {
                width: 600px !important;
            }

            .u-row .u-col {
                vertical-align: top;
            }

            .u-row .u-col-33p33 {
                width: 199.98px !important;
            }

            .u-row .u-col-66p67 {
                width: 400.02px !important;
            }

            .u-row .u-col-100 {
                width: 600px !important;
            }

        }

        @media (max-width: 620px) {
            .u-row-container {
                max-width: 100% !important;
                padding-left: 0px !important;
                padding-right: 0px !important;
            }

            .u-row .u-col {
                min-width: 320px !important;
                max-width: 100% !important;
                display: block !important;
            }

            .u-row {
                width: calc(100% - 40px) !important;
            }

            .u-col {
                width: 100% !important;
            }

            .u-col > div {
                margin: 0 auto;
            }
        }

        body {
            margin: 0;
            padding: 0;
        }

        table,
        tr,
        td {
            vertical-align: top;
            border-collapse: collapse;
        }

        p {
            margin: 0;
        }

        .ie-container table,
        .mso-container table {
            table-layout: fixed;
        }

        * {
            line-height: inherit;
        }

        a[x-apple-data-detectors='true'] {
            color: inherit !important;
            text-decoration: none !important;
        }

    </style>"""
    email_template = textwrap.dedent('''\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <!--[if !mso]><!-->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
    <title></title>

    {0}


    <!--[if !mso]><!-->
    <link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css">
    <!--<![endif]-->

</head>

<body class="clean-body u_body"
      style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #ffffff;color: #000000">
<!--[if IE]>
<div class="ie-container"><![endif]-->
<!--[if mso]>
<div class="mso-container"><![endif]-->
<table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #ffffff;width:100%"
       cellpadding="0" cellspacing="0">
    <tbody>
    <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
            <!--[if (mso)|(IE)]>
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td align="center" style="background-color: #ffffff;"><![endif]-->


            <div class="u-row-container" style="padding: 0px;background-color: transparent">
                <div class="u-row"
                     style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #483fa8;">
                    <div style="border-collapse: collapse;display: table;width: 100%;background-image: url('https://api.treatsnmore.ug/img/email/image-3.png');background-repeat: no-repeat;background-position: center top;background-color: transparent;">
                        <!--[if (mso)|(IE)]>
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td style="padding: 0px;background-color: transparent;" align="center">
                                    <table cellpadding="0" cellspacing="0" border="0" style="width:600px;">
                                        <tr style="background-image: url('images/image-3.png');background-repeat: no-repeat;background-position: center top;background-color: #483fa8;">
                        <![endif]-->

                        <!--[if (mso)|(IE)]>
                        <td align="center" width="600"
                            style="width: 600px;padding: 0px 0px 42px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"
                            valign="top"><![endif]-->
                        <div class="u-col u-col-100"
                             style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
                            <div style="width: 100% !important;">
                                <!--[if (!mso)&(!IE)]><!-->
                                <div style="padding: 0px 0px 42px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                                    <!--<![endif]-->

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:35px 40px 10px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                    <tr>
                                                        <td style="padding-right: 0px;padding-left: 0px;" align="left">

                                                            <img align="left" border="0" src="{1}"
                                                                 alt="Treats 'N More Logo" title="Logo"
                                                                 style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 26%;max-width: 135.2px;"
                                                                 width="135.2"/>

                                                        </td>
                                                    </tr>
                                                </table>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:8px 40px 0px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div style="color: #ffffff; line-height: 140%; text-align: left; word-wrap: break-word;">
                                                    <p style="font-size: 14px; line-height: 140%;"><span
                                                            style="font-size: 48px; line-height: 67.2px;"><strong><span
                                                            style="line-height: 67.2px; font-size: 48px;">Notify Me</span></strong></span>
                                                    </p>
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 40px 25px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div style="color: #fcfcfc; line-height: 170%; text-align: left; word-wrap: break-word;">
                                                    <p style="line-height: 170%; font-size: 14px;"><span
                                                            style="font-size: 18px; line-height: 30.6px;">Request to be notified when more inventory is added</span>
                                                    </p>
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 10px 40px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div align="left">
                                                    <!--[if mso]>
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                                           style="border-spacing: 0; border-collapse: collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;font-family:'Raleway',sans-serif;">
                                                        <tr>
                                                            <td style="font-family:'Raleway',sans-serif;" align="left">
                                                                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
                                                                             xmlns:w="urn:schemas-microsoft-com:office:word"
                                                                             href=""
                                                                             style="height:50px; v-text-anchor:middle; width:225px;"
                                                                             arcsize="80%" stroke="f"
                                                                             fillcolor="#fcfcfc">
                                                                    <w:anchorlock/>
                                                                    <center style="color:#38389b;font-family:'Raleway',sans-serif;">
                                                    <![endif]-->
                                                    <a href="{2}" target="_blank"
                                                       style="box-sizing: border-box;display: inline-block;font-family:'Raleway',sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #38389b; background-color: #fcfcfc; border-radius: 40px;-webkit-border-radius: 40px; -moz-border-radius: 40px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;">
                                                        <span style="display:block;padding:14px 55px;line-height:120%;"><span
                                                                style="font-size: 18px; line-height: 21.6px;"><strong><span
                                                                style="line-height: 21.6px; font-size: 18px;">View Product</span></strong></span></span>
                                                    </a>
                                                    <!--[if mso]></center></v:roundrect></td></tr></table><![endif]-->
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                    </div>
                </div>
            </div>


            <div class="u-row-container" style="padding: 0px;background-color: transparent">
                <div class="u-row"
                     style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f9f9f9;">
                    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
                        <!--[if (mso)|(IE)]>
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td style="padding: 0px;background-color: transparent;" align="center">
                                    <table cellpadding="0" cellspacing="0" border="0" style="width:600px;">
                                        <tr style="background-color: #f9f9f9;"><![endif]-->

                        <!--[if (mso)|(IE)]>
                        <td align="center" width="400"
                            style="width: 400px;padding: 30px 30px 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"
                            valign="top"><![endif]-->
                        <div class="u-col u-col-66p67"
                             style="max-width: 320px;min-width: 400px;display: table-cell;vertical-align: top;">
                            <div style="width: 100% !important;">
                                <!--[if (!mso)&(!IE)]><!-->
                                <div style="padding: 30px 30px 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                                    <!--<![endif]-->

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 0px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div style="color: #483fa8; line-height: 140%; text-align: left; word-wrap: break-word;">
                                                    <p style="font-size: 14px; line-height: 140%; text-align: center;">
                                                        <span style="font-size: 24px; line-height: 33.6px;"><strong><span
                                                                style="line-height: 33.6px; font-size: 24px;">Hi {3},</span></strong></span>
                                                    </p>
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div style="color: #868990; line-height: 170%; text-align: left; word-wrap: break-word;">
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;">We shall notify you as soon</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;"> as we add new products for</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;">{4}</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        &nbsp;</p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;">Thanks for getting in touch</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        &nbsp;</p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;">Summary:</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;">Product: {5}</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        <span style="font-size: 16px; line-height: 27.2px;">Quantity: {6}</span>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 170%; text-align: center;">
                                                        &nbsp;</p>
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]>
                        <td align="center" width="200"
                            style="width: 200px;padding: 30px 30px 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"
                            valign="top"><![endif]-->
                        <div class="u-col u-col-33p33"
                             style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                            <div style="width: 100% !important;">
                                <!--[if (!mso)&(!IE)]><!-->
                                <div style="padding: 30px 30px 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                                    <!--<![endif]-->

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                    <tr>
                                                        <td style="padding-right: 0px;padding-left: 0px;"
                                                            align="center">

                                                            <img align="center" border="0" src="{7}"
                                                                 alt="{8}" title="{9}"
                                                                 style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 200px;"
                                                                 width="200"/>

                                                        </td>
                                                    </tr>
                                                </table>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                    </div>
                </div>
            </div>


            <div class="u-row-container" style="padding: 0px;background-color: transparent">
                <div class="u-row"
                     style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f1f1f1;">
                    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
                        <!--[if (mso)|(IE)]>
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td style="padding: 0px;background-color: transparent;" align="center">
                                    <table cellpadding="0" cellspacing="0" border="0" style="width:600px;">
                                        <tr style="background-color: #f1f1f1;"><![endif]-->

                        <!--[if (mso)|(IE)]>
                        <td align="center" width="600"
                            style="width: 600px;padding: 20px 30px 34px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"
                            valign="top"><![endif]-->
                        <div class="u-col u-col-100"
                             style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
                            <div style="width: 100% !important;">
                                <!--[if (!mso)&(!IE)]><!-->
                                <div style="padding: 20px 30px 34px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                                    <!--<![endif]-->

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 10px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div style="color: #483fa8; line-height: 140%; text-align: left; word-wrap: break-word;">
                                                    <p style="line-height: 140%; text-align: center; font-size: 14px;">
                                                        <span style="font-size: 24px; line-height: 33.6px;"><strong>Treats 'N More {10}</strong></span>
                                                    </p>
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <table height="0px" align="center" border="0" cellpadding="0"
                                                       cellspacing="0" width="100%"
                                                       style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #b4b0e6;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
                                                    <tbody>
                                                    <tr style="vertical-align: top">
                                                        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
                                                            <span>&#160;</span>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <div style="color: #4e4d52; line-height: 140%; text-align: center; word-wrap: break-word;">
                                                    <p style="font-size: 14px; line-height: 140%;">Phone:
                                                        0200909059<br/>email: <a rel="noopener"
                                                                                 href="mailto:support@treatsnmore.ug"
                                                                                 target="_blank">support@treatsnmore.ug</a>
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 140%;">Location: TNP House,
                                                        Plot 328, Block22, Kiwatule - Ntinda</p>
                                                    <p style="font-size: 14px; line-height: 140%;">$time</p>
                                                </div>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                                           cellspacing="0" width="100%" border="0">
                                        <tbody>
                                        <tr>
                                            <td style="overflow-wrap:break-word;word-break:break-word;padding:23px 40px 10px;font-family:'Raleway',sans-serif;"
                                                align="left">

                                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                    <tr>
                                                        <td style="padding-right: 0px;padding-left: 0px;"
                                                            align="center">

                                                            <img align="center" border="0" src="{11}"
                                                                 alt="Treats 'N More Logo" title="Treats 'N More Logo"
                                                                 style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 34%;max-width: 176.8px;"
                                                                 width="176.8"/>

                                                        </td>
                                                    </tr>
                                                </table>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>

                                    <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                            </div>
                        </div>
                        <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                    </div>
                </div>
            </div>


            <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
        </td>
    </tr>
    </tbody>
</table>
<!--[if mso]></div><![endif]-->
<!--[if IE]></div><![endif]-->
</body>

</html>
''').format(styles, notification['treatsnmore_logo'], notification['product_link'], notification['name'], notification['product_name'], notification['product_name'], notification['quantity'], notification['product_image'], notification['product_name'], notification['product_name'], notification['country'], notification['treatsnmore_logo'])
    return email_template


# define receipients based on country
async def country_receipients(country, user_name, user_email):

    # default receipients
    receipients = [
        {"Email": user_email, "Name": user_name},
        {"Email": "support@treatsnmore.ug", "Name": "Treats N More"},
        {"Email": "ivilleinc@gmail.com", "Name": "Echeru Rodney"},
        {"Email": "rodneyecheru@gmail.com", "Name": "Echeru Rodney"},
        {"Email": "emmanuelkakooza@gmail.com", "Name": "Kakooza Emmanuel"},
        {"Email": "ruthmugoya@gmail.com", "Name": "Mugoya Ruth"},
        {"Email": "denluk07@yahoo.com", "Name": "Lukhoola Dennis"},
        {"Email": "denluk07@gmail.com", "Name": "Lukhoola Dennis"},
    ]

    # add email recipients based on country
    if country == "Kenya":
        receipients += [
            {"Email": "paulmunyao@hotmail.com", "Name": "Paul Munyao"},
            {"Email": "mwendwa.mutwii@gmail.com", "Name": "Mwendwa Mutwii"},
        ]

    return receipients


# define spam receipients
async def spam_receipients(country, user_name, user_email):

    # default receipients
    return [
        {"Email": "support@treatsnmore.ug", "Name": "Treats N More"},
        {"Email": "ivilleinc@gmail.com", "Name": "Echeru Rodney"},
        {"Email": "rodneyecheru@gmail.com", "Name": "Echeru Rodney"},
        {"Email": "emmanuelkakooza@gmail.com", "Name": "Kakooza Emmanuel"},
    ]


# send email notification
async def notification_request(notification):
    api_key = '6dcf89455b68f0d237db383cb34aba08'
    api_secret = '50af08652e1b2f0f512e2cd3da0ffbdc'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    email_template = await notification_template(notification)
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "support@treatsnmore.ug",
                    "Name": "Treats N More"
                },
                "To": await country_receipients(notification['country'], notification['name'], notification['email'], ),
                "Subject": f"Stock request for {notification['quantity']} {notification['product_name']}",
                "TextPart": "Platform email",
                "HTMLPart": email_template,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    pass


@api.get("/")
def welcome():
    return {
        "message": "You have reached email endpoint, define resources to serve",
        "status": "info",
        "data_status": False
    }
