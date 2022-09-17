using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace Divar.Web.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            //Response.Cookies.Delete("SelectCity");
            if (Request.Cookies["SelectCity"] == null)
                return View("FirstIndex");


            return View();
        }

        public IActionResult SelectCity(string cityName)
        {
            DateTime date;
            if (DateTime.Now.Month + 1 > 12)
                date = DateTime.Parse($"{DateTime.Now.Year + 1}/{(DateTime.Now.Month + 1 > 12 ? DateTime.Now.Month - 11 : DateTime.Now.Month + 1)}/{DateTime.Now.Day}");
            else
                date = DateTime.Parse($"{DateTime.Now.Year}/{(DateTime.Now.Month + 1 > 12 ? DateTime.Now.Month - 11 : DateTime.Now.Month + 1)}/{DateTime.Now.Day}");

            Response.Cookies.Append("SelectCity", cityName, new CookieOptions() { Expires = date });

            return RedirectToAction("Index");
        }
    }
}