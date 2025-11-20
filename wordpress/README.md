# Special-Auto.ro: Ultra-Optimized WordPress Store for Low-End Hosting  
*Truck parts e-commerce (Romania) - engineered to thrive on 0.5GHz CPU / 800MB RAM shared hosting (2025)*  

![Site Preview]
https://imgur.com/a/JHwt5X7
---

## ⚙️ The Challenge  
Running a **fully functional WordPress e-commerce site** on notoriously underpowered shared hosting (typical Romanian budget providers):  
- **CPU**: 0.5 GHz (single-core, throttled)  
- **RAM**: ~800 MB (with 128MB PHP memory limit)  
- **No VPS/Cloud options** due to legacy business constraints  
- **Critical requirement**: Maintain SEO rankings while operating on hardware weaker than a 2010 smartphone  

---

## 🚀 Key Optimizations  

### LiteSpeed Cache Mastery  
- **100% cache hit ratio** via tuned `.htaccess` rules and LSCWP plugin config  
- **Zero dynamic PHP execution** on cached pages (verified via server logs)  
- **Guest Mode** enabled: 99% of visitors never trigger PHP  
- **Object cache** with LiteSpeed Memcached (even on shared hosting)  

### Custom-Built Systems (No Bloated Plugins)  
All critical features developed from scratch to avoid plugin overhead:  
- **Live Stock Checker** → AJAX-driven inventory API (≤5KB payloads)  
- **SEO Schema Generator** → Dynamic JSON-LD without third-party libraries  
- **Image Optimizer** → On-upload WebP conversion + responsive srcset (pure PHP)  

### WordPress Hardening  
```php  
// wp-config.php snippet  
define('WP_MEMORY_LIMIT', '96M');  
define('WP_POST_REVISIONS', 2);  
define('EMPTY_TRASH_DAYS', 1);  
add_filter('jpeg_quality', fn() => 75);  
