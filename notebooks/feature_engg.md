# Feature Analysis and Engineering Report

---

## SECTION 1: INITIAL FEATURE LIST
The following 30 features were initially identified for analysis, alongside the target variable.

| ID | Feature Name | ID | Feature Name |
| :--- | :--- | :--- | :--- |
| 1 | having_IP_Address | 16 | SFH |
| 2 | URL_Length | 17 | Submitting_to_email |
| 3 | Shortining_Service | 18 | Abnormal_URL |
| 4 | having_At_Symbol | 19 | Redirect |
| 5 | double_slash_redirecting | 20 | on_mouseover |
| 6 | Prefix_Suffix | 21 | RightClick |
| 7 | having_Sub_Domain | 22 | popUpWidnow |
| 8 | SSLfinal_State | 23 | Iframe |
| 9 | Domain_registeration_length | 24 | age_of_domain |
| 10 | Favicon | 25 | DNSRecord |
| 11 | port | 26 | web_traffic |
| 12 | HTTPS_token | 27 | Page_Rank |
| 13 | Request_URL | 28 | Google_Index |
| 14 | URL_of_Anchor | 29 | Links_pointing_to_page |
| 15 | Links_in_tags | 30 | Statistical_report |
| **T** | **Result (Target)** | | |

---

## SECTION 2: FINAL FEATURE LIST
*Post-selection and engineering phase.*

### Kept Individual Features
1. **SSLfinal_State**
2. **URL_of_Anchor**
3. **having_Sub_Domain**
4. **web_traffic**
5. **Request_URL**

### Engineered Features
6. **url_obfuscation_score**
7. **ui_deception_score**
8. **trust_score**
9. **redirection_risk_score**

### Target Variable
10. **Result**

---

## SECTION 3: FEATURE ENGINEERING FORMULAS

### 1. url_obfuscation_score
> **Formula:** `Shortining_Service` + `double_slash_redirecting` + `having_At_Symbol` + `Prefix_Suffix`

* **Reasoning:** These features represent URL manipulation techniques used to confuse users. They are highly correlated and describe the same underlying phishing behavior.

### 2. ui_deception_score
> **Formula:** `on_mouseover` + `RightClick` + `popUpWidnow` + `Iframe`

* **Reasoning:** These represent deceptive client-side UI or JavaScript behaviors. Strong inter-correlation indicates these features are redundant when kept separate.

### 3. trust_score
> **Formula:** `SSLfinal_State` + `HTTPS_token` + `Google_Index`

* **Reasoning:** These indicate the legitimacy and trustworthiness of a website. Combining them creates a more robust and reliable trust signal.

### 4. redirection_risk_score
> **Formula:** `Redirect` + `Submitting_to_email` + `Abnormal_URL`

* **Reasoning:** These features capture suspicious redirection or abnormal navigation patterns, jointly highlighting phishing intent.

---

## SECTION 4: DROPPED FEATURES AND REASONS

**Dropped Features:**
* `URL_Length`, `Domain_registeration_length`, `Favicon`, `port`, `Links_in_tags`, `SFH`, `age_of_domain`, `DNSRecord`, `Page_Rank`, `Links_pointing_to_page`, `Statistical_report`.

**Reasons for Exclusion:**
* **Low Correlation:** Very weak relationship with the target variable.
* **Predictive Power:** Limited effectiveness when used in binary form.
* **Model Health:** Dropping these reduces noise and multicollinearity, improving model generalization.

---

## SECTION 5: PREPROCESSING NOTE

> All features were converted to a **binary (0/1) format** by mapping "-1" values to "0". This standardization ensures consistent interpretability of correlations and improves overall model stability.

---

## SECTION 6: SUMMARY

* **Efficiency:** Reduced total feature count while preserving semantic meaning.
* **Optimization:** Minimized multicollinearity for cleaner statistical analysis.
* **Robustness:** Engineered features align closely with domain-specific phishing knowledge.