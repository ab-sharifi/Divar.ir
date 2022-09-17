using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class States
    {
        [Key]
        public int Id { get; set; }

        [Display(Name = "نام استان")]
        public string StateName { get; set; }

        public virtual IEnumerable<Cities> Cities { get; set; }
    }
}
