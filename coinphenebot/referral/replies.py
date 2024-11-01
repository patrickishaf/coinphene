def get_ref_link_reply(link: str, earnings: float, referral_count: int = 0):
    return (f"*Referrals:*\n\nYour reflink: [{link}]({link})\n\nReferrals: *{referral_count}*\n\nLifetime SOL earned: *{earnings}*\n\n"
            f"Refer your friends and earn 30% of their fees in the first month, 20% in the second and 10% forever!")